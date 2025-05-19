import streamlit as st
import numpy as np
from PIL import Image
import cv2
import io
import zipfile
import os
import tempfile
from string_art_generator import StringArtGenerator, StringArtConfig

def main():
    st.set_page_config(
        page_title="String Art Generator",
        page_icon="🎨",
        layout="wide"
    )
    
    st.title("🎨 String Art Generator")
    st.markdown("Transform your images into beautiful string art patterns!")
    
    # Sidebar for parameters
    st.sidebar.header("String Art Parameters")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload an image",
        type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
        help="Upload an image to convert to string art"
    )
    
    # Parameters
    num_pins = st.sidebar.slider(
        "Number of pins",
        min_value=50,
        max_value=400,
        value=200,
        step=10,
        help="More pins = finer detail but longer generation time"
    )
    
    num_connections = st.sidebar.slider(
        "Number of connections",
        min_value=500,
        max_value=10000,
        value=3000,
        step=100,
        help="More connections = more detailed result but longer generation time"
    )
    
    canvas_size = st.sidebar.selectbox(
        "Canvas size (pixels)",
        options=[600, 800, 1000, 1200],
        index=1,
        help="Higher resolution = better quality but slower generation"
    )
    
    string_opacity = st.sidebar.slider(
        "String opacity",
        min_value=0.1,
        max_value=1.0,
        value=0.3,
        step=0.05,
        help="How dark each string appears (lower = more subtle)"
    )
    
    # Advanced settings
    with st.sidebar.expander("Advanced Settings"):
        pin_radius = st.slider(
            "Pin radius (visualization only)",
            min_value=1,
            max_value=8,
            value=3,
            help="Size of pins in the visualization"
        )
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Original Image")
        if uploaded_file is not None:
            # Display original image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Preview processed image
            image_array = np.array(image.convert('L'))
            image_resized = cv2.resize(image_array, (canvas_size, canvas_size))
            
            # Apply circular mask for preview
            center = canvas_size // 2
            radius = center - 50
            y, x = np.ogrid[:canvas_size, :canvas_size]
            mask = (x - center) ** 2 + (y - center) ** 2 <= radius ** 2
            image_masked = image_resized * mask
            
            st.image(image_masked, caption="Processed (circular crop)", use_container_width=True)
        else:
            st.info("Please upload an image to get started!")
            st.markdown("### Tips for best results:")
            st.markdown("""
            - **High contrast images** work best
            - **Simple subjects** with clear edges
            - **Black and white or monochrome** images often produce better results
            - **Portraits and simple shapes** are ideal subjects
            """)
    
    with col2:
        st.header("String Art Result")
        
        if uploaded_file is not None:
            # Generate button
            if st.button("🎨 Generate String Art", type="primary", use_container_width=True):
                # Convert uploaded image to array
                image = Image.open(uploaded_file)
                image_array = np.array(image.convert('L'))
                
                # Create config
                config = StringArtConfig(
                    num_pins=num_pins,
                    num_connections=num_connections,
                    canvas_size=canvas_size,
                    pin_radius=pin_radius,
                    string_opacity=string_opacity
                )
                
                # Generate string art
                with st.spinner("Generating string art... This may take a few minutes."):
                    generator = StringArtGenerator(config)
                    canvas, connections = generator.generate_string_art(image_array=image_array)
                    
                    # Create visualization
                    viz_image = generator.create_visualization(connections)
                    
                    # Store results in session state
                    st.session_state['string_art_result'] = viz_image
                    st.session_state['connections'] = connections
                    st.session_state['config'] = config
                    st.session_state['canvas'] = canvas
                    st.session_state['generator'] = generator
        
        # Display results if available
        if 'string_art_result' in st.session_state:
            st.image(st.session_state['string_art_result'], 
                    caption="Generated String Art", 
                    use_container_width=True)
            
            # Statistics
            st.success(f"✅ Generated {len(st.session_state['connections'])} connections using {st.session_state['config'].num_pins} pins")
            
            # Download section
            st.header("Download Files")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                # Download visualization
                img_buffer = io.BytesIO()
                st.session_state['string_art_result'].save(img_buffer, format='PNG')
                st.download_button(
                    label="📥 Download Image",
                    data=img_buffer.getvalue(),
                    file_name="string_art_visualization.png",
                    mime="image/png",
                    use_container_width=True
                )
            
            with col_b:
                # Download connections as JSON
                connections_data = {
                    'connections': [0] + st.session_state['connections'],
                    'num_pins': st.session_state['config'].num_pins,
                    'num_connections': len(st.session_state['connections']),
                    'instructions': 'Start at pin 0, then follow the sequence. Each number represents the next pin to connect to.',
                    'format': 'Continuous path - connect pin 0 to pin connections[0], then to connections[1], etc.'
                }
                
                st.download_button(
                    label="📥 Download JSON",
                    data=str(connections_data).replace("'", '"'),
                    file_name="string_art_connections.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col_c:
                # Download connections as text
                full_sequence = [0] + st.session_state['connections']
                text_content = f"""String Art Connection Sequence

Number of pins: {st.session_state['config'].num_pins}
Number of connections: {len(st.session_state['connections'])}
Canvas size: {st.session_state['config'].canvas_size}x{st.session_state['config'].canvas_size}

Instructions:
Start at pin 0, then follow the sequence below.
Each number represents the next pin to connect to.

Connection sequence:
{', '.join(map(str, full_sequence))}

Pin Layout:
Pins are arranged in a circle, numbered 0 to {st.session_state['config'].num_pins - 1} clockwise starting from the rightmost point (3 o'clock position).
"""
                
                st.download_button(
                    label="📥 Download Text",
                    data=text_content,
                    file_name="string_art_connections.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    # Information section
    st.header("How it works")
    with st.expander("Algorithm Details"):
        st.markdown("""
        The string art generator uses a **greedy algorithm** to create the best possible representation:
        
        1. **Image Preprocessing**: The uploaded image is converted to grayscale, resized, and masked to fit within a circle
        
        2. **Pin Placement**: Pins are evenly distributed around the circle's perimeter
        
        3. **String Selection**: The algorithm iteratively selects the next string connection that will:
           - Add the most "darkness" to areas that should be dark in the target image
           - Create the best match between the current canvas and target image
        
        4. **Continuous Path**: All strings form one continuous path, making it practical to create in real life
        
        **Tips for physical construction:**
        - Use a circular wooden board or embroidery hoop
        - Mark pin positions evenly around the perimeter
        - Use thin black thread or string
        - Follow the connection sequence exactly for best results
        """)
    
    with st.expander("Parameter Guide"):
        st.markdown("""
        **Number of Pins (50-400)**:
        - Fewer pins = simpler, more abstract result
        - More pins = finer detail and smoother curves
        - Recommended: 150-250 for most images
        
        **Number of Connections (500-10000)**:
        - Fewer connections = lighter, more minimalist result
        - More connections = darker, more detailed result
        - Recommended: 2000-4000 for good balance
        
        **String Opacity (0.1-1.0)**:
        - Lower values = each string adds less darkness
        - Higher values = each string adds more darkness
        - Adjust based on your physical string thickness
        """)

if __name__ == "__main__":
    main()
