import os
import UnityPy
import zlib

input_dir = "assets/android/gameassetbundles"
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
                    name_lower = data.name.lower()
                    if "items" in name_lower:
                        raw_bytes = data.script
                        try:
                            decompressed = zlib.decompress(raw_bytes)
                            content = decompressed
                        except:
                            content = raw_bytes
                        output_path = os.path.join(output_dir, data.name + ".json")
                        with open(output_path, "wb") as f:
                            f.write(content)
                        print(f"[SAVED] {data.name} extracted and decompressed to {output_path}")
        except:
            pass

print("استخراج وفك ضغط جميع ملفات items انتهى.")