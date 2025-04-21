import nibabel as nib
import gc
from CTPA_App_Frontend.utils.notification import add_notification

def load_nifti_scan(file_path):
    """
    Load a NIfTI scan from a file
    
    Parameters:
    -----------
    file_path : str
        The path to the NIfTI file
        
    Returns:
    --------
    nibabel.Nifti1Image or None
        The loaded NIfTI image, or None if loading failed
    """
    if not file_path:
        return None
        
    try:
        img = nib.load(file_path)
        return img
    except Exception as e:
        add_notification(f"Error loading scan: {str(e)}", "error")
        return None

def get_scan_data(nifti_img):
    """
    Extract data from a NIfTI image
    
    Parameters:
    -----------
    nifti_img : nibabel.Nifti1Image
        The NIfTI image to extract data from
        
    Returns:
    --------
    numpy.ndarray
        The scan data as a numpy array
    """
    try:
        scan_data = nifti_img.get_fdata()
        # Free memory
        del nifti_img
        gc.collect()
        return scan_data
    except Exception as e:
        add_notification(f"Error extracting scan data: {str(e)}", "error")
        return None