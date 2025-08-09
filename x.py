import subprocess
import sys

try:
    import lz4.frame
except ImportError:
    print("lz4 غير مثبت، سيتم التثبيت الآن...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "lz4"])
    import lz4.frame

import os
import UnityPy
import zlib

input_dir = "assets/android/gameassetbundles/config"
output_dir = "extracted_json"

os.makedirs(output_dir, exist_ok=True)

for dirpath, _, filenames in os.walk(input_dir):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)
        try:
            env = UnityPy.load(file_path)
            for obj in env.objects:
                if obj.type.name == "TextAsset":
                    data = obj.read()
                    raw_bytes = data.script
                    content = None
                    try:
                        content = zlib.decompress(raw_bytes)
                        print(f"[ZLIB decompressed] {data.name}")
                    except:
                        try:
                            content = lz4.frame.decompress(raw_bytes)
                            print(f"[LZ4 decompressed] {data.name}")
                        except:
                            content = raw_bytes
                            print(f"[No decompression] {data.name}")
                    output_path = os.path.join(output_dir, data.name + ".json")
                    with open(output_path, "wb") as f:
                        f.write(content)
        except Exception:
            pass

print("استخراج وفك ضغط ملفات JSON من مجلد config انتهى.")
