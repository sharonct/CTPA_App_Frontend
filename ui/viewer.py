import streamlit as st
from api.client import get_scan_slice

def display_window_controls():
    """Display window controls and handle window settings"""
    # Window controls container
    st.markdown("### Window Settings")
    
    # Window presets
    cols = st.columns(4)
    with cols[0]:
        if st.button("PE Protocol", use_container_width=True, type="primary"):
            st.session_state.window_center = 100
            st.session_state.window_width = 700
            st.rerun()
    with cols[1]:
        if st.button("Pulmonary", use_container_width=True):
            st.session_state.window_center = -600
            st.session_state.window_width = 1500
            st.rerun()
    with cols[2]:
        if st.button("Mediastinal", use_container_width=True):
            st.session_state.window_center = 40
            st.session_state.window_width = 400
            st.rerun()
    with cols[3]:
        if st.button("Bone", use_container_width=True):
            st.session_state.window_center = 500
            st.session_state.window_width = 2000
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

def display_scan_views(scan_id, metadata):
    """Display the scan views based on the current view"""
    # Get dimensions from metadata
    if not metadata or "dimensions" not in metadata or not metadata["dimensions"]:
        st.warning("Scan dimensions not available")
        return
    
    dims = metadata["dimensions"]
    
    # Create view buttons
    display_view_controls()
    
    # Window controls
    display_window_controls()
    
    current_view = st.session_state.current_view
    
    # Set slice parameters based on view
    if current_view == 'axial':
        max_slice = dims[2] - 1 if len(dims) > 2 else 0
        # Initialize axial_slice in session_state if not present
        if 'axial_slice' not in st.session_state:
            st.session_state.axial_slice = max_slice // 2
        # Use the value from session_state for the slider
        slice_idx = st.slider('Navigate Slices', 0, max_slice, st.session_state.axial_slice, key='axial_nav')
        # Store the value back to session_state, but only if changed
        if slice_idx != st.session_state.axial_slice:
            st.session_state.axial_slice = slice_idx
            st.rerun()
        view_label = "Axial View"
    elif current_view == 'sagittal':
        max_slice = dims[0] - 1 if len(dims) > 0 else 0
        # Initialize sagittal_slice in session_state if not present
        if 'sagittal_slice' not in st.session_state:
            st.session_state.sagittal_slice = max_slice // 2
        # Use the value from session_state for the slider
        slice_idx = st.slider('Navigate Slices', 0, max_slice, st.session_state.sagittal_slice, key='sagittal_nav')
        # Store the value back to session_state, but only if changed
        if slice_idx != st.session_state.sagittal_slice:
            st.session_state.sagittal_slice = slice_idx
            st.rerun()
        view_label = "Sagittal View"
    else:  # coronal
        max_slice = dims[1] - 1 if len(dims) > 1 else 0
        # Initialize coronal_slice in session_state if not present
        if 'coronal_slice' not in st.session_state:
            st.session_state.coronal_slice = max_slice // 2
        # Use the value from session_state for the slider
        slice_idx = st.slider('Navigate Slices', 0, max_slice, st.session_state.coronal_slice, key='coronal_nav')
        # Store the value back to session_state, but only if changed
        if slice_idx != st.session_state.coronal_slice:
            st.session_state.coronal_slice = slice_idx
            st.rerun()
        view_label = "Coronal View"
    
    # Get the slice
    slice_data = get_scan_slice(
        scan_id, 
        current_view, 
        slice_idx, 
        st.session_state.window_center, 
        st.session_state.window_width
    )
    
    if slice_data and "image" in slice_data:
        # Display the image
        st.image(slice_data["image"], caption=f"{view_label} - Slice {slice_idx}", use_container_width=True)
    else:
        st.error("Failed to load scan slice")

def render_viewer_section(scan_id, metadata):
    """Render the scan viewer section"""
    # Initialize session state variables if not present
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'axial'
    if 'window_center' not in st.session_state:
        st.session_state.window_center = 100  # Default to PE Protocol settings
    if 'window_width' not in st.session_state:
        st.session_state.window_width = 700
    
    # Scan visualization section heading
    st.markdown("""
    <h3 style="color: black; margin: 0;">🩺 CTPA Visualization</h3>
    """, unsafe_allow_html=True)
    
    # Display scan views
    display_scan_views(scan_id, metadata)