"""
Setup script to save the cat image for Siya
Instructions: Place your cat image as 'cat_source.png' or 'cat_source.jpg' in this folder
"""

from PIL import Image
from pathlib import Path

def setup_cat_image():
    """Setup the cat image for the application"""
    
    # Check for source image
    source_files = ['cat_source.png', 'cat_source.jpg', 'cat_source.jpeg', 'cat_image.png', 'cat_image.jpg']
    source_path = None
    
    for filename in source_files:
        path = Path(filename)
        if path.exists():
            source_path = path
            break
    
    if not source_path:
        print("❌ No cat image found!")
        print("\n📋 Instructions:")
        print("1. Save your cat image as 'cat_source.png' (or .jpg)")
        print("2. Place it in the same folder as this script")
        print("3. Run this script again")
        print("\n💡 Or: The app will create a placeholder cat automatically")
        return False
    
    try:
        # Load and optimize image
        print(f"📷 Loading image from: {source_path}")
        img = Image.open(source_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            print("🔄 Converting image to RGB...")
            img = img.convert('RGB')
        
        # Resize to reasonable size if too large
        max_size = (800, 800)
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            print(f"📐 Resizing image from {img.size} to fit {max_size}...")
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save as cat_image.png
        output_path = Path("cat_image.png")
        print(f"💾 Saving as: {output_path}")
        img.save(output_path, 'PNG', optimize=True)
        
        print("✅ Cat image setup complete!")
        print(f"📏 Final size: {img.size}")
        print("\n🎉 You can now run: python siya_image.py")
        return True
        
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return False


if __name__ == "__main__":
    print("🐱 Siya Cat Image Setup")
    print("=" * 40)
    print()
    
    success = setup_cat_image()
    
    if not success:
        print("\n💡 Tip: You can still run the app!")
        print("It will create a cute placeholder cat automatically.")
    
    input("\nPress Enter to exit...")
