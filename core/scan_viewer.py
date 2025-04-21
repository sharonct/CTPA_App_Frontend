import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def apply_window(img_data, window_center, window_width):
    """
    Apply windowing to an image
    
    Parameters:
    -----------
    img_data : numpy.ndarray
        The image data
    window_center : int
        The window center (HU)
    window_width : int
        The window width (HU)
        
    Returns:
    --------
    numpy.ndarray
        The windowed image
    """
    img = img_data.copy()
    min_value = window_center - window_width // 2
    max_value = window_center + window_width // 2
    img[img < min_value] = min_value
    img[img > max_value] = max_value
    img = (img - min_value) / (max_value - min_value) * 255
    return img

def display_window_controls():
    """Display window controls and handle window settings"""
    # Window controls container
    st.markdown("<div class='window-control'>", unsafe_allow_html=True)
    st.markdown("### Window Settings")
    
    # Window presets
    cols = st.columns(4)
    with cols[0]:
        if st.button("Pulmonary", use_container_width=True):
            st.session_state.window_center = -600
            st.session_state.window_width = 1500
            st.rerun()
    with cols[1]:
        if st.button("Mediastinal", use_container_width=True):
            st.session_state.window_center = 40
            st.session_state.window_width = 400
            st.rerun()
    with cols[2]:
        if st.button("Bone", use_container_width=True):
            st.session_state.window_center = 500
            st.session_state.window_width = 2000
            st.rerun()
    with cols[3]:
        if st.button("PE Protocol", use_container_width=True):
            st.session_state.window_center = 100
            st.session_state.window_width = 700
            st.rerun()
    
    # Custom window controls
    cols = st.columns(2)
    with cols[0]:
        window_center = st.slider("Window Center (HU)", -1000, 1000, st.session_state.window_center, 10)
        if window_center != st.session_state.window_center:
            st.session_state.window_center = window_center
            st.rerun()
    
    with cols[1]:
        window_width = st.slider("Window Width (HU)", 1, 4000, st.session_state.window_width, 50)
        if window_width != st.session_state.window_width:
            st.session_state.window_width = window_width
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def display_view_controls():
    """Display view controls for axial, sagittal, and coronal planes"""
    cols = st.columns(3)
    
    with cols[0]:
        axial_button = st.button('Axial View', key='axial_btn', 
                               type="primary" if st.session_state.current_view == 'axial' else "secondary",
                               use_container_width=True)
        if axial_button:
            st.session_state.current_view = 'axial'
            st.rerun()
            
    with cols[1]:
        sagittal_button = st.button('Sagittal View', key='sagittal_btn', 
                                  type="primary" if st.session_state.current_view == 'sagittal' else "secondary",
                                  use_container_width=True)
        if sagittal_button:
            st.session_state.current_view = 'sagittal'
            st.rerun()
            
    with cols[2]:
        coronal_button = st.button('Coronal View', key='coronal_btn', 
                                 type="primary" if st.session_state.current_view == 'coronal' else "secondary",
                                 use_container_width=True)
        if coronal_button:
            st.session_state.current_view = 'coronal'
            st.rerun()
    
    # Add spacing
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

def display_navigation_controls(current_view, dims):
    """
    Display slice navigation controls
    
    Parameters:
    -----------
    current_view : str
        The current view ('axial', 'sagittal', or 'coronal')
    dims : tuple
        The dimensions of the scan data
    """
    st.markdown("### Navigation Controls")
    cols = st.columns(3)
    
    with cols[0]:
        if st.button("⬅️ Previous Slice"):
            if current_view == 'axial' and st.session_state['axial_slice'] > 0:
                st.session_state['axial_slice'] -= 1
            elif current_view == 'sagittal' and st.session_state['sagittal_slice'] > 0:
                st.session_state['sagittal_slice'] -= 1
            elif current_view == 'coronal' and st.session_state['coronal_slice'] > 0:
                st.session_state['coronal_slice'] -= 1
            st.rerun()
    
    with cols[1]:
        if st.button("Reset View"):
            if current_view == 'axial':
                st.session_state['axial_slice'] = dims[2] // 2
            elif current_view == 'sagittal':
                st.session_state['sagittal_slice'] = dims[0] // 2
            else:  # coronal
                st.session_state['coronal_slice'] = dims[1] // 2
            st.rerun()
    
    with cols[2]:
        if st.button("Next Slice ➡️"):
            if current_view == 'axial' and st.session_state['axial_slice'] < dims[2] - 1:
                st.session_state['axial_slice'] += 1
            elif current_view == 'sagittal' and st.session_state['sagittal_slice'] < dims[0] - 1:
                st.session_state['sagittal_slice'] += 1
            elif current_view == 'coronal' and st.session_state['coronal_slice'] < dims[1] - 1:
                st.session_state['coronal_slice'] += 1
            st.rerun()

def display_scan_views(scan_data):
    """
    Display the scan views and controls
    
    Parameters:
    -----------
    scan_data : numpy.ndarray
        The scan data to display
    """
    # Get dimensions
    dims = scan_data.shape
    
    # Create view buttons
    display_view_controls()
    
    # Window controls
    display_window_controls()
    
    # Get current view and set up slider
    current_view = st.session_state.current_view
    
    # Set slider parameters based on view
    if current_view == 'axial':
        max_slice = dims[2] - 1
        default_slice = dims[2] // 2
        if 'axial_slice' not in st.session_state:
            st.session_state.axial_slice = default_slice
        slice_idx = st.slider('Navigate Slices', 0, max_slice, st.session_state.axial_slice, key='axial_slice')
        slice_img = scan_data[:, :, slice_idx].T
        view_label = "Axial View - Slice"
    elif current_view == 'sagittal':
        max_slice = dims[0] - 1
        default_slice = dims[0] // 2
        if 'sagittal_slice' not in st.session_state:
            st.session_state.sagittal_slice = default_slice
        slice_idx = st.slider('Navigate Slices', 0, max_slice, st.session_state.sagittal_slice, key='sagittal_slice')
        slice_img = scan_data[slice_idx, :, :].T
        view_label = "Sagittal View - Slice"
    else:  # coronal
        max_slice = dims[1] - 1
        default_slice = dims[1] // 2
        if 'coronal_slice' not in st.session_state:
            st.session_state.coronal_slice = default_slice
        slice_idx = st.slider('Navigate Slices', 0, max_slice, st.session_state.coronal_slice, key='coronal_slice')
        slice_img = scan_data[:, slice_idx, :].T
        view_label = "Coronal View - Slice"
    
    # Apply windowing
    slice_img = apply_window(slice_img, st.session_state.window_center, st.session_state.window_width)
    
    # Display the slice with improved visualization
    fig, ax = plt.subplots(figsize=(8, 8))
    img = ax.imshow(slice_img, cmap='bone')
    ax.set_title(f"{view_label} {slice_idx}", fontsize=14)
    ax.axis('off')
    
    # Add ruler/scale for better interpretation
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    
    # Add image navigation controls
    display_navigation_controls(current_view, dims)