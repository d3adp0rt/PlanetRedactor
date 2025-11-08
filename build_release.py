import os
import shutil
import sys
import subprocess
from datetime import datetime

def create_executable():
    print("\nCreating executable...")
    try:
        subprocess.run([
            'pyinstaller',
            '--onefile',
            '--noconsole',
            '--name', 'PlanetRedactor',
            'Gui.py'
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating executable: {e}")
        return False
    except FileNotFoundError:
        print("Error: PyInstaller not found. Please install it using: pip install pyinstaller")
        return False

def create_release(version):
    # Base paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    release_dir = os.path.join(base_dir, 'releases', f'v{version}')
    
    # Create release directory structure
    os.makedirs(release_dir, exist_ok=True)
    os.makedirs(os.path.join(release_dir, 'textures'), exist_ok=True)
    os.makedirs(os.path.join(release_dir, 'mods'), exist_ok=True)
    
    # Python files to copy
    python_files = [
        'Buildings.py',
        'Gui.py',
        'GuiMethods.py',
        'Landscapes.py',
        'Planet.py',
        'PlanetGenerator.py',
        'PlanetTypes.py'
    ]
    
    # Copy Python files
    print("Copying Python files...")
    for file in python_files:
        src = os.path.join(base_dir, file)
        dst = os.path.join(release_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {file}")
        else:
            print(f"Warning: {file} not found")
    
    # Copy textures
    print("\nCopying textures...")
    textures_src = os.path.join(base_dir, 'textures')
    textures_dst = os.path.join(release_dir, 'textures')
    if os.path.exists(textures_src):
        for item in os.listdir(textures_src):
            s = os.path.join(textures_src, item)
            d = os.path.join(textures_dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
                print(f"Copied texture folder: {item}")
            elif item.lower().endswith('.png'):
                shutil.copy2(s, d)
                print(f"Copied texture file: {item}")
    
    # Copy mods structure
    print("\nCopying mods structure...")
    mods_src = os.path.join(base_dir, 'mods')
    mods_dst = os.path.join(release_dir, 'mods')
    if os.path.exists(mods_src):
        shutil.copytree(mods_src, mods_dst, dirs_exist_ok=True)
        print("Copied mods structure")
    
    # Copy README and LICENSE
    print("\nCopying documentation...")
    for doc in ['README.md', 'LICENSE']:
        src = os.path.join(base_dir, doc)
        dst = os.path.join(release_dir, doc)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {doc}")
    
    # Create and copy executable
    if create_executable():
        # Copy the executable to release directory
        exe_src = os.path.join(base_dir, 'dist', 'PlanetRedactor.exe')
        exe_dst = os.path.join(release_dir, 'PlanetRedactor.exe')
        if os.path.exists(exe_src):
            shutil.copy2(exe_src, exe_dst)
            print("\nCopied executable to release directory")
        
        # Clean up PyInstaller files
        print("\nCleaning up build files...")
        build_dir = os.path.join(base_dir, 'build')
        dist_dir = os.path.join(base_dir, 'dist')
        spec_file = os.path.join(base_dir, 'PlanetRedactor.spec')
        
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir)
        if os.path.exists(spec_file):
            os.remove(spec_file)
    
    # Create ZIP archive
    print("\nCreating ZIP archive...")
    release_name = f"PlanetRedactor_v{version}"
    zip_path = os.path.join(os.path.dirname(release_dir), f"{release_name}.zip")
    
    try:
        shutil.make_archive(
            os.path.join(os.path.dirname(release_dir), release_name),
            'zip',
            release_dir
        )
        print(f"Created ZIP archive: {zip_path}")
        
        # Remove release directory after successful ZIP creation
        print("\nCleaning up release directory...")
        shutil.rmtree(release_dir)
        print(f"Release directory removed")
        
        print(f"\nRelease v{version} has been created successfully!")
        print(f"ZIP archive location: {zip_path}")
    except Exception as e:
        print(f"Error creating ZIP archive: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python build_release.py VERSION")
        print("Example: python build_release.py 1.0.1")
        sys.exit(1)
    
    version = sys.argv[1]
    create_release(version)