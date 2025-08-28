#!/usr/bin/env python3
import argparse, os, shutil, sys
from pathlib import Path

TEMPLATE_CONFIG = """<?xml version="1.0"?>
<model>
  <name>{name}</name>
  <version>1.0</version>
  <sdf version="1.7">model.sdf</sdf>
  <author><name>generated</name></author>
  <description>ArUco sticker plane from {img}</description>
</model>
"""

TEMPLATE_SDF = """<?xml version="1.0"?>
<sdf version="1.7">
  <model name="{name}">
    <static>true</static>
    <link name="link">
      <visual name="vis">
        <double_sided>true</double_sided>
        <cast_shadows>false</cast_shadows>
        <geometry>
          <plane>
            <normal>1 0 0</normal>
            <size>{size_m} {size_m}</size>
          </plane>
        </geometry>
        <material>
          <pbr>
            <metal>
              <albedo>1 1 1 1</albedo>
              <albedo_map>materials/textures/{img_name}</albedo_map>
              <roughness>1.0</roughness>
              <metalness>0.0</metalness>
            </metal>
          </pbr>
        </material>
      </visual>
      <collision name="col">
        <geometry>
          <box>
            <size>{thick_m} {size_m} {size_m}</size>
          </box>
        </geometry>
      </collision>
    </link>
  </model>
</sdf>
"""

def main():
    ap = argparse.ArgumentParser(description="Generate Ignition sticker-plane models from images")
    ap.add_argument("-i","--images-dir", required=True, help="Folder with PNG/JPG marker images")
    ap.add_argument("-g","--gazebo-dir", required=True, help="Output Gazebo models directory")
    ap.add_argument("-s","--size-mm", type=float, default=200.0, help="Sticker size (square) in mm")
    ap.add_argument("--thickness-mm", type=float, default=2.0, help="Collision thickness in mm")
    ap.add_argument("--prefix", default="aruco_", help="Model name prefix")
    args = ap.parse_args()

    src = Path(os.path.expandvars(args.images_dir)).expanduser()
    out = Path(os.path.expandvars(args.gazebo_dir)).expanduser()
    if not src.is_dir():
        sys.exit(f"Images dir not found: {src}")
    out.mkdir(parents=True, exist_ok=True)

    size_m = args.size_mm / 1000.0
    thick_m = max(args.thickness_mm / 1000.0, 0.001)

    exts = (".png",".jpg",".jpeg",".JPG",".PNG",".JPEG")
    imgs = sorted([p for p in src.iterdir() if p.suffix in exts])
    if not imgs:
        sys.exit(f"No images (*.png/jpg) found in {src}")

    for img in imgs:
        stem = img.stem  # filename without extension
        model_name = f"{args.prefix}{stem}".replace(" ","_")
        model_dir = out / model_name
        tex_dir = model_dir / "materials" / "textures"
        tex_dir.mkdir(parents=True, exist_ok=True)
        # copy texture (keep original name)
        shutil.copy2(str(img), str(tex_dir / img.name))
        # write model.config
        (model_dir / "model.config").write_text(TEMPLATE_CONFIG.format(name=model_name, img=img.name))
        # write model.sdf
        (model_dir / "model.sdf").write_text(TEMPLATE_SDF.format(
            name=model_name, img_name=img.name, size_m=f"{size_m:.6f}", thick_m=f"{thick_m:.6f}"
        ))
        print(f"Created model: {model_name}")

    print(f"Done. Add to IGN_GAZEBO_RESOURCE_PATH: {out}")

if __name__ == "__main__":
    main()
