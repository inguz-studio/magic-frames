#!/usr/bin/env python3
"""Generate an editable CapCut draft from a JSON timeline specification."""

from __future__ import annotations

import argparse
import difflib
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

import pycapcut as capcut


DEFAULT_DRAFTS_DIR = "~/Movies/CapCut/User Data/Projects/com.lveditor.draft"
RECOMMENDED_MEDIA_ROOT = "~/Movies/magic-frames/<project>/"
VIDEO_TRACK_PREFIX = "inserts"
TEXT_TRACK_PREFIX = "texts"
AUDIO_TRACK_PREFIX = "audio"


class SpecError(ValueError):
    """Raised when a timeline specification is invalid."""


@dataclass(frozen=True)
class MediaReference:
    field: str
    path: Path


def seconds(value: Any, field: str, *, minimum: float = 0.0, strict: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SpecError(f"{field} must be a number in seconds")
    number = float(value)
    if (strict and number <= minimum) or (not strict and number < minimum):
        relation = "greater than" if strict else "at least"
        raise SpecError(f"{field} must be {relation} {minimum}")
    return number


def integer(value: Any, field: str, *, minimum: int = 1) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise SpecError(f"{field} must be an integer of at least {minimum}")
    return value


def boolean(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise SpecError(f"{field} must be a boolean")
    return value


def mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SpecError(f"{field} must be an object")
    return value


def sequence(value: Any, field: str) -> list[Any]:
    if not isinstance(value, list):
        raise SpecError(f"{field} must be an array")
    return value


def required_string(obj: dict[str, Any], key: str, field: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SpecError(f"{field}.{key} must be a non-empty string")
    return value


def resolve_absolute_media_path(raw: Any, field: str) -> Path:
    if not isinstance(raw, str) or not raw.strip():
        raise SpecError(f"{field} must be a non-empty absolute path")
    unexpanded = Path(raw)
    if not unexpanded.is_absolute():
        raise SpecError(
            f"{field} must be an absolute path; move media to {RECOMMENDED_MEDIA_ROOT}"
        )
    path = unexpanded.resolve(strict=False)
    if not path.exists() or not path.is_file():
        raise SpecError(f"{field} does not exist or is not a file: {path}")

    home = Path.home().resolve()
    blocked_roots = [home / name for name in ("Desktop", "Documents", "Downloads")]
    for blocked in blocked_roots:
        try:
            path.relative_to(blocked)
        except ValueError:
            continue
        raise SpecError(
            f"{field} is under macOS-protected folder {blocked}. "
            f"Move it to {RECOMMENDED_MEDIA_ROOT}"
        )
    return path


def resolve_enum(enum_type: Any, raw: Any, field: str) -> Any:
    if not isinstance(raw, str) or not raw:
        raise SpecError(f"{field} must be a non-empty {enum_type.__name__} member name")
    members = enum_type.__members__
    if raw in members:
        return members[raw]
    suggestions = difflib.get_close_matches(raw, list(members), n=20, cutoff=0.0)
    shown = ", ".join(suggestions)
    raise SpecError(
        f"Invalid {enum_type.__name__} name for {field}: {raw!r}. "
        f"20 closest names: {shown}"
    )


def parse_hex_color(raw: Any, field: str) -> tuple[float, float, float]:
    if not isinstance(raw, str):
        raise SpecError(f"{field} must be a #RRGGBB color")
    value = raw.removeprefix("#")
    if len(value) != 6:
        raise SpecError(f"{field} must be a #RRGGBB color")
    try:
        channels = tuple(int(value[index : index + 2], 16) / 255 for index in (0, 2, 4))
    except ValueError as exc:
        raise SpecError(f"{field} must be a #RRGGBB color") from exc
    return channels  # type: ignore[return-value]


def parse_animation(
    obj: dict[str, Any], key: str, enum_type: Any, field: str
) -> tuple[Any, float | None] | None:
    raw = obj.get(key)
    if raw is None:
        return None
    if isinstance(raw, str):
        return resolve_enum(enum_type, raw, f"{field}.{key}"), None
    animation = mapping(raw, f"{field}.{key}")
    enum_name = animation.get("type", animation.get("name"))
    enum_value = resolve_enum(enum_type, enum_name, f"{field}.{key}.type")
    duration = animation.get("duration")
    parsed_duration = (
        seconds(duration, f"{field}.{key}.duration", strict=True) if duration is not None else None
    )
    return enum_value, parsed_duration


def time_range(start: float, duration: float) -> Any:
    return capcut.trange(f"{start:.6f}s", f"{duration:.6f}s")


def validate_interval_fields(item: dict[str, Any], field: str) -> tuple[float, float, float]:
    source_in = seconds(item.get("in"), f"{field}.in")
    source_out = seconds(item.get("out"), f"{field}.out", strict=True)
    at = seconds(item.get("at"), f"{field}.at")
    if source_out <= source_in:
        raise SpecError(f"{field}.out must be greater than {field}.in")
    return source_in, source_out, at


def allocate_lanes(intervals: Sequence[tuple[float, float]]) -> list[int]:
    lane_ends: list[float] = []
    assignments: list[int] = []
    for start, end in intervals:
        selected = next((index for index, lane_end in enumerate(lane_ends) if start >= lane_end), None)
        if selected is None:
            selected = len(lane_ends)
            lane_ends.append(end)
        else:
            lane_ends[selected] = end
        assignments.append(selected)
    return assignments


def ensure_no_overlap(intervals: Sequence[tuple[float, float]], field: str) -> None:
    ordered = sorted(intervals)
    for previous, current in zip(ordered, ordered[1:]):
        if current[0] < previous[1]:
            raise SpecError(
                f"{field} overlap on the main track: {previous[0]:g}-{previous[1]:g}s "
                f"and {current[0]:g}-{current[1]:g}s"
            )


def load_spec(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise SpecError(f"Timeline file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SpecError(f"Invalid JSON in {path}: {exc}") from exc
    return mapping(data, "timeline")


def validate_spec(spec: dict[str, Any]) -> tuple[dict[str, Any], list[MediaReference]]:
    name = required_string(spec, "name", "timeline")
    if name in {".", ".."} or name != Path(name).name or "/" in name or "\\" in name:
        raise SpecError("timeline.name must be a safe folder name without path separators")

    width = integer(spec.get("width"), "timeline.width")
    height = integer(spec.get("height"), "timeline.height")
    fps = integer(spec.get("fps"), "timeline.fps")
    clips = sequence(spec.get("clips"), "timeline.clips")
    if not clips:
        raise SpecError("timeline.clips must contain at least one main-track clip")
    inserts = sequence(spec.get("inserts", []), "timeline.inserts")
    texts = sequence(spec.get("texts", []), "timeline.texts")
    audio = sequence(spec.get("audio", []), "timeline.audio")

    normalized: dict[str, Any] = {
        "name": name,
        "width": width,
        "height": height,
        "fps": fps,
        "drafts_dir": str(Path(os.path.expanduser(spec.get("drafts_dir", DEFAULT_DRAFTS_DIR))).resolve()),
        "clips": [],
        "inserts": [],
        "texts": [],
        "audio": [],
        "filter": None,
        "srt": None,
    }
    media: list[MediaReference] = []

    main_intervals: list[tuple[float, float]] = []
    for index, raw_item in enumerate(clips):
        field = f"timeline.clips[{index}]"
        item = mapping(raw_item, field)
        path = resolve_absolute_media_path(item.get("path"), f"{field}.path")
        source_in, source_out, at = validate_interval_fields(item, field)
        speed = seconds(item.get("speed", 1.0), f"{field}.speed", strict=True)
        volume = seconds(item.get("volume", 1.0), f"{field}.volume")
        duration = (source_out - source_in) / speed
        transition = None
        if item.get("transition_out") is not None:
            transition_obj = mapping(item["transition_out"], f"{field}.transition_out")
            transition_name = transition_obj.get("type", transition_obj.get("name"))
            transition = {
                "type": resolve_enum(
                    capcut.TransitionType, transition_name, f"{field}.transition_out.type"
                ),
                "duration": seconds(
                    transition_obj.get("duration"),
                    f"{field}.transition_out.duration",
                    strict=True,
                ),
            }
        effect = (
            resolve_enum(capcut.VideoSceneEffectType, item["effect"], f"{field}.effect")
            if item.get("effect") is not None
            else None
        )
        normalized["clips"].append(
            {
                "path": path,
                "source_in": source_in,
                "source_out": source_out,
                "at": at,
                "duration": duration,
                "speed": speed,
                "volume": volume,
                "transition": transition,
                "effect": effect,
                "intro": parse_animation(item, "intro", capcut.IntroType, field),
                "outro": parse_animation(item, "outro", capcut.OutroType, field),
            }
        )
        media.append(MediaReference(f"{field}.path", path))
        main_intervals.append((at, at + duration))

    if min(start for start, _ in main_intervals) != 0:
        raise SpecError("The first main-track clip must start at timeline.clips[].at = 0")
    ensure_no_overlap(main_intervals, "timeline.clips")

    for index, raw_item in enumerate(inserts):
        field = f"timeline.inserts[{index}]"
        item = mapping(raw_item, field)
        path = resolve_absolute_media_path(item.get("path"), f"{field}.path")
        source_in, source_out, at = validate_interval_fields(item, field)
        duration = source_out - source_in
        scale = seconds(item.get("scale", 1.0), f"{field}.scale", strict=True)
        x = seconds(item.get("x", 0.0), f"{field}.x", minimum=-10.0)
        y = seconds(item.get("y", 0.0), f"{field}.y", minimum=-10.0)
        normalized["inserts"].append(
            {
                "path": path,
                "source_in": source_in,
                "source_out": source_out,
                "at": at,
                "duration": duration,
                "scale": scale,
                "x": x,
                "y": y,
            }
        )
        media.append(MediaReference(f"{field}.path", path))

    for index, raw_item in enumerate(texts):
        field = f"timeline.texts[{index}]"
        item = mapping(raw_item, field)
        text = required_string(item, "text", field)
        at = seconds(item.get("at"), f"{field}.at")
        duration = seconds(item.get("duration"), f"{field}.duration", strict=True)
        border_raw = mapping(item.get("border", {"color": "#000000", "width": 0}), f"{field}.border")
        border_width = seconds(border_raw.get("width", 0), f"{field}.border.width")
        normalized["texts"].append(
            {
                "text": text,
                "at": at,
                "duration": duration,
                "size": seconds(item.get("size", 8), f"{field}.size", strict=True),
                "bold": boolean(item.get("bold", False), f"{field}.bold"),
                "color": parse_hex_color(item.get("color", "#FFFFFF"), f"{field}.color"),
                "border": (
                    capcut.TextBorder(
                        color=parse_hex_color(border_raw.get("color", "#000000"), f"{field}.border.color"),
                        width=border_width,
                    )
                    if border_width > 0
                    else None
                ),
                "y": seconds(item.get("y", 0.0), f"{field}.y", minimum=-10.0),
                "intro": parse_animation(item, "intro", capcut.TextIntro, field),
                "outro": parse_animation(item, "outro", capcut.TextOutro, field),
            }
        )

    for index, raw_item in enumerate(audio):
        field = f"timeline.audio[{index}]"
        item = mapping(raw_item, field)
        path = resolve_absolute_media_path(item.get("path"), f"{field}.path")
        source_in, source_out, at = validate_interval_fields(item, field)
        normalized["audio"].append(
            {
                "path": path,
                "source_in": source_in,
                "source_out": source_out,
                "at": at,
                "duration": source_out - source_in,
                "volume": seconds(item.get("volume", 1.0), f"{field}.volume"),
            }
        )
        media.append(MediaReference(f"{field}.path", path))

    if spec.get("filter") is not None:
        filter_obj = mapping(spec["filter"], "timeline.filter")
        normalized["filter"] = {
            "type": resolve_enum(capcut.FilterType, filter_obj.get("type"), "timeline.filter.type"),
            "intensity": seconds(filter_obj.get("intensity", 100), "timeline.filter.intensity"),
        }
        if normalized["filter"]["intensity"] > 100:
            raise SpecError("timeline.filter.intensity must be between 0 and 100")

    if spec.get("srt") is not None:
        srt = resolve_absolute_media_path(spec["srt"], "timeline.srt")
        normalized["srt"] = srt

    return normalized, media


def apply_animation(segment: Any, animation: tuple[Any, float | None] | None) -> None:
    if animation is None:
        return
    enum_value, duration = animation
    if duration is None:
        segment.add_animation(enum_value)
    else:
        segment.add_animation(enum_value, duration=f"{duration:.6f}s")


def build_script(spec: dict[str, Any]) -> Any:
    script = capcut.ScriptFile(spec["width"], spec["height"], spec["fps"])
    script.add_track(capcut.TrackType.video, "main", relative_index=0)

    video_materials: dict[Path, Any] = {}
    audio_materials: dict[Path, Any] = {}

    def video_material(path: Path) -> Any:
        if path not in video_materials:
            video_materials[path] = capcut.VideoMaterial(str(path))
        return video_materials[path]

    def audio_material(path: Path) -> Any:
        if path not in audio_materials:
            audio_materials[path] = capcut.AudioMaterial(str(path))
        return audio_materials[path]

    for item in spec["clips"]:
        source_duration = item["source_out"] - item["source_in"]
        segment = capcut.VideoSegment(
            video_material(item["path"]),
            time_range(item["at"], item["duration"]),
            source_timerange=time_range(item["source_in"], source_duration),
            speed=item["speed"],
            volume=item["volume"],
        )
        if item["transition"]:
            segment.add_transition(
                item["transition"]["type"], duration=f"{item['transition']['duration']:.6f}s"
            )
        if item["effect"]:
            segment.add_effect(item["effect"])
        apply_animation(segment, item["intro"])
        apply_animation(segment, item["outro"])
        script.add_segment(segment, "main")

    insert_lanes = allocate_lanes(
        [(item["at"], item["at"] + item["duration"]) for item in spec["inserts"]]
    )
    for lane in sorted(set(insert_lanes)):
        script.add_track(capcut.TrackType.video, f"{VIDEO_TRACK_PREFIX}-{lane + 1}", relative_index=lane + 1)
    for item, lane in zip(spec["inserts"], insert_lanes):
        segment = capcut.VideoSegment(
            video_material(item["path"]),
            time_range(item["at"], item["duration"]),
            source_timerange=time_range(item["source_in"], item["duration"]),
            clip_settings=capcut.ClipSettings(
                scale_x=item["scale"],
                scale_y=item["scale"],
                transform_x=item["x"],
                transform_y=item["y"],
            ),
        )
        script.add_segment(segment, f"{VIDEO_TRACK_PREFIX}-{lane + 1}")

    text_lanes = allocate_lanes(
        [(item["at"], item["at"] + item["duration"]) for item in spec["texts"]]
    )
    for lane in sorted(set(text_lanes)):
        script.add_track(capcut.TrackType.text, f"{TEXT_TRACK_PREFIX}-{lane + 1}", relative_index=lane)
    for item, lane in zip(spec["texts"], text_lanes):
        segment = capcut.TextSegment(
            item["text"],
            time_range(item["at"], item["duration"]),
            style=capcut.TextStyle(
                size=item["size"], bold=item["bold"], color=item["color"]
            ),
            border=item["border"],
            clip_settings=capcut.ClipSettings(transform_y=item["y"]),
        )
        apply_animation(segment, item["intro"])
        apply_animation(segment, item["outro"])
        script.add_segment(segment, f"{TEXT_TRACK_PREFIX}-{lane + 1}")

    audio_lanes = allocate_lanes(
        [(item["at"], item["at"] + item["duration"]) for item in spec["audio"]]
    )
    for lane in sorted(set(audio_lanes)):
        script.add_track(capcut.TrackType.audio, f"{AUDIO_TRACK_PREFIX}-{lane + 1}", relative_index=lane)
    for item, lane in zip(spec["audio"], audio_lanes):
        segment = capcut.AudioSegment(
            audio_material(item["path"]),
            time_range(item["at"], item["duration"]),
            source_timerange=time_range(item["source_in"], item["duration"]),
            volume=item["volume"],
        )
        script.add_segment(segment, f"{AUDIO_TRACK_PREFIX}-{lane + 1}")

    if spec["srt"] is not None:
        script.import_srt(str(spec["srt"]), "subtitles")

    if spec["filter"] is not None:
        script.add_track(capcut.TrackType.filter, "filter", relative_index=0)
        if script.duration <= 0:
            raise SpecError("Cannot add a timeline filter to a zero-duration draft")
        script.add_filter(
            spec["filter"]["type"],
            capcut.trange("0s", script.duration),
            "filter",
            intensity=spec["filter"]["intensity"],
        )
    return script


def capcut_warning() -> str | None:
    try:
        result = subprocess.run(
            ["pgrep", "-x", "CapCut"], capture_output=True, text=True, check=False
        )
    except OSError:
        return "Could not check whether CapCut is running (pgrep unavailable)."
    if result.returncode == 0:
        return "CapCut is running. Close it before generating or replacing a draft."
    return None


def infer_project_root(media: Iterable[MediaReference]) -> Path:
    paths = [str(reference.path) for reference in media if reference.field != "timeline.srt"]
    if not paths:
        return Path("/")
    common = Path(os.path.commonpath(paths))
    return common.parent if common.is_file() or len(paths) == 1 else common


def write_portable_helpers(draft_dir: Path, media: list[MediaReference]) -> None:
    project_root = infer_project_root(media)
    mappings: list[dict[str, str]] = []
    seen: set[Path] = set()
    for reference in media:
        if reference.path in seen:
            continue
        seen.add(reference.path)
        try:
            relative = reference.path.relative_to(project_root)
        except ValueError:
            relative = Path(reference.path.name)
        mappings.append({"original": str(reference.path), "relative": str(relative)})

    (draft_dir / "media-paths.json").write_text(
        json.dumps({"source_project_root": str(project_root), "media": mappings}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    readme = """# Como abrir este rascunho no CapCut

1. Copie as mídias preservando a estrutura de pastas registrada em `media-paths.json`.
2. Nesta pasta, execute `python3 relink.py /caminho/absoluto/da/nova/pasta-do-projeto`.
3. Copie esta pasta inteira para `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/`.
4. Feche o CapCut antes da cópia e abra o aplicativo depois.

O relink exige que todas as mídias existam no novo destino. Ele atualiza
`draft_content.json` e `draft_info.json` juntos e nunca toca em `root_meta_info.json`.
"""
    (draft_dir / "README-abrir.md").write_text(readme, encoding="utf-8")
    relink_source = '''#!/usr/bin/env python3
"""Relink this portable CapCut draft to a new project media root."""

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", help="Absolute root containing the copied media")
    args = parser.parse_args()
    root = Path(args.project_root)
    if not root.is_absolute():
        parser.error("project_root must be an absolute path")
    root = root.resolve()
    base = Path(__file__).resolve().parent
    mapping = json.loads((base / "media-paths.json").read_text(encoding="utf-8"))
    replacements = {}
    missing = []
    for entry in mapping["media"]:
        target = (root / entry["relative"]).resolve()
        replacements[entry["original"]] = str(target)
        if not target.is_file():
            missing.append(str(target))
    if missing:
        raise SystemExit("Missing media at the new root:\\n- " + "\\n- ".join(missing))

    content_path = base / "draft_content.json"
    content = json.loads(content_path.read_text(encoding="utf-8"))
    changed = 0
    for collection in ("videos", "audios"):
        for material in content.get("materials", {}).get(collection, []):
            old = material.get("path")
            if old in replacements:
                material["path"] = replacements[old]
                changed += 1
    encoded = json.dumps(content, ensure_ascii=False, separators=(",", ":"))
    content_path.write_text(encoded, encoding="utf-8")
    (base / "draft_info.json").write_text(encoded, encoding="utf-8")
    print(f"Relinked {changed} material record(s) to {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''
    relink_path = draft_dir / "relink.py"
    relink_path.write_text(relink_source, encoding="utf-8")
    relink_path.chmod(0o755)


def save_draft(
    script: Any,
    spec: dict[str, Any],
    media: list[MediaReference],
    output_base: Path,
    *,
    replace: bool,
    portable: bool,
) -> Path:
    output_base.mkdir(parents=True, exist_ok=True)
    draft_dir = output_base / spec["name"]
    if draft_dir.exists() and not replace:
        raise SpecError(f"Draft already exists: {draft_dir}. Use --replace to overwrite it.")
    folder = capcut.DraftFolder(str(output_base))
    created = folder.create_draft(
        spec["name"], spec["width"], spec["height"], spec["fps"], allow_replace=replace
    )
    script.save_path = created.save_path
    script.save()
    content_path = draft_dir / "draft_content.json"
    shutil.copyfile(content_path, draft_dir / "draft_info.json")
    if portable:
        write_portable_helpers(draft_dir, media)
    return draft_dir


def track_summary(script: Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    for track in script.tracks.values():
        key = track.track_type.name
        counts[key] = counts.get(key, 0) + 1
    return counts


def print_summary(
    spec: dict[str, Any], script: Any, media: list[MediaReference], draft_dir: Path | None, warnings: list[str]
) -> None:
    print("CapCut draft summary")
    print(f"Name: {spec['name']}")
    print(f"Canvas: {spec['width']}x{spec['height']} @ {spec['fps']} fps")
    print(f"Mode: {'check only' if draft_dir is None else 'generated'}")
    if draft_dir is not None:
        print(f"Draft: {draft_dir}")
    counts = track_summary(script)
    print("Tracks: " + ", ".join(f"{key}={value}" for key, value in sorted(counts.items())))
    print(f"Segments: {sum(len(track.segments) for track in script.tracks.values())}")
    print("Media:")
    for path in dict.fromkeys(reference.path for reference in media):
        print(f"  - {path} [exists={'yes' if path.is_file() else 'no'}]")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print("Warnings: none")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("timeline", type=Path, help="Path to timeline.json")
    parser.add_argument("--check", action="store_true", help="Validate without writing a draft")
    parser.add_argument("--out", type=Path, help="Write a portable draft under this directory")
    parser.add_argument("--replace", action="store_true", help="Replace an existing draft with the same name")
    args = parser.parse_args(argv)
    if args.check and args.out:
        parser.error("--check and --out cannot be used together")
    if args.check and args.replace:
        parser.error("--replace has no effect with --check")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        raw_spec = load_spec(args.timeline.resolve())
        spec, media = validate_spec(raw_spec)
        script = build_script(spec)
        warnings = [warning for warning in [capcut_warning()] if warning]
        for warning in warnings:
            print(f"WARNING: {warning}", file=sys.stderr)
        if args.check:
            print_summary(spec, script, media, None, warnings)
            return 0

        output_base = args.out.resolve() if args.out else Path(spec["drafts_dir"])
        draft_dir = save_draft(
            script,
            spec,
            media,
            output_base,
            replace=args.replace,
            portable=args.out is not None,
        )
        print_summary(spec, script, media, draft_dir, warnings)
        return 0
    except (SpecError, FileExistsError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
