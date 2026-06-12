import os
import hashlib
import cv2
import numpy as np
from pathlib import Path
from pdf2image import convert_from_path
from skimage.metrics import structural_similarity as ssim
from tqdm import tqdm

# --- CONFIGURATION ---
TOLERANCE = 0.998  # 98% similarity threshold for MATLAB PDFs
DPI = 200          # Quality for rendering PDFs to images

def get_file_hash(path):
    """Generates an MD5 hash for fast text/binary comparison (used for .tex files)."""
    hasher = hashlib.md5()
    with open(path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def crop_to_content(gray_img):
    """Crops out the white margins MATLAB often leaves around plots."""
    _, thresh = cv2.threshold(gray_img, 254, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(np.vstack(contours))
        return gray_img[y:y+h, x:x+w]
    return gray_img

def compare_pdfs(pdf1, pdf2):
    """Compares two PDFs visually using SSIM to account for MATLAB variations."""
    try:
        img1 = np.array(convert_from_path(pdf1, dpi=DPI)[0].convert('L'))
        img2 = np.array(convert_from_path(pdf2, dpi=DPI)[0].convert('L'))
        
        img1_c = crop_to_content(img1)
        img2_c = crop_to_content(img2)
        
        if img1_c.shape != img2_c.shape:
            img2_c = cv2.resize(img2_c, (img1_c.shape[1], img1_c.shape[0]))
            
        score, _ = ssim(img1_c, img2_c, full=True)
        return score >= TOLERANCE, score
    except Exception as e:
        return False, f"Error processing PDF: {str(e)}"

def scan_directory(base_dir):
    """Scans directory recursively and returns relative paths of valid files."""
    base_path = Path(base_dir)
    valid_extensions = {'.tex', '.pdf'}
    file_set = set()
    
    for file_path in base_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in valid_extensions:
            # Store the path relative to the base directory for easy comparison
            relative_path = file_path.relative_to(base_path)
            file_set.add(relative_path)
    return file_set

def compare_directories(dir_test, dir_sections):
    path_test = Path(dir_test)
    path_sections = Path(dir_sections)
    
    print("Scanning directories...")
    files_test = scan_directory(path_test)
    files_sections = scan_directory(path_sections)
    
    # Structural breakdowns
    all_shared_paths = files_test.intersection(files_sections)
    only_in_test = files_test - files_sections
    only_in_sections = files_sections - files_test
    
    matched = []
    mismatched = []
    
    print(f"Comparing {len(all_shared_paths)} shared files...")
    # Using tqdm for a nice progress bar during heavy PDF calculations
    for rel_path in tqdm(all_shared_paths, desc="Checking contents"):
        file_test = path_test / rel_path
        file_sections = path_sections / rel_path
        
        if rel_path.suffix.lower() == '.tex':
            # Fast text check
            if get_file_hash(file_test) == get_file_hash(file_sections):
                matched.append((rel_path, "100% Hash Match"))
            else:
                mismatched.append((rel_path, "Text content changed"))
                
        elif rel_path.suffix.lower() == '.pdf':
            # Visual graph check
            is_match, score_info = compare_pdfs(file_test, file_sections)
            if is_match:
                matched.append((rel_path, f"Visual Match ({score_info*100:.1f}%)"))
            else:
                score_str = f"{score_info*100:.1f}%" if isinstance(score_info, float) else str(score_info)
                mismatched.append((rel_path, f"Visual Mismatch (Score: {score_str})"))

    # --- PRINT REPORT ---
    print("\n" + "="*50)
    print("                   COMPARISON REPORT                  ")
    print("="*50)
    
    print(f"\n✅ MATCHED FILES ({len(matched)}):")
    for item, detail in matched:
        print(f"  • {item} [{detail}]")
        
    print(f"\n❌ MISMATCHED CONTENT ({len(mismatched)}):")
    for item, detail in mismatched:
        print(f"  • {item} --> Reason: {detail}")
        
    print(f"\n⚠️ EXTRA IN TEST / MISSING IN SECTIONS ({len(only_in_test)}):")
    for item in only_in_test:
        print(f"  • {item}")
        
    print(f"\n⚠️ EXTRA IN SECTIONS / MISSING IN TEST ({len(only_in_sections)}):")
    for item in only_in_sections:
        print(f"  • {item}")
        
    print("\n" + "="*50)

if __name__ == "__main__":
    # Update these paths to target your actual folders
    TEST_DIR = "./results"
    SECTIONS_DIR = "../sections/results"
    
    if os.path.exists(TEST_DIR) and os.path.exists(SECTIONS_DIR):
        compare_directories(TEST_DIR, SECTIONS_DIR)
    else:
        print("Error: Please verify that both directory paths exist.")