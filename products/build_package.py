"""
Project TENKA - Product Packaging Engine
Packages all monetization products into a deployable digital asset (.zip).
"""

import os
import zipfile

def build():
    products_dir = "C:/Users/haruki/.gemini/antigravity/scratch/project_tenka/products"
    zip_path = os.path.join(products_dir, "TENKA_MONETIZATION_PACKAGE.zip")

    files_to_pack = [
        "TENKA_COMPLETE_APPLICATION_TEMPLATE.md",
        "TENKA_UNCONTESTED_TENDER_DATABASE.csv"
    ]

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files_to_pack:
            file_path = os.path.join(products_dir, f)
            if os.path.exists(file_path):
                zf.write(file_path, arcname=f)
                print(f"  + パッケージ同梱: {f}")

    print(f"\n[OK] デジタル商品パッケージ生成完了: {zip_path}")
    print(f"ファイルサイズ: {os.path.getsize(zip_path)} bytes")

if __name__ == "__main__":
    build()
