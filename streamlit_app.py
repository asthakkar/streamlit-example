import streamlit as st
import numpy as np
from streamlit_cropper import st_cropper
from PIL import Image
from PIL import ImageOps
import rembg
import os

st.set_option('deprecation.showfileUploaderEncoding', False)
# Upload an image and set some options for demo purposes
st.header("Test App")
img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])
realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
stroke_width = st.sidebar.number_input(label="Box Thickness", value=3, step=1)

aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
aspect_dict = {
    "1:1": (1, 1),
    "16:9": (16, 9),
    "4:3": (4, 3),
    "2:3": (2, 3),
    "Free": None
}
aspect_ratio = aspect_dict[aspect_choice]

return_type_choice = st.sidebar.radio(label="Return type", options=["Cropped image", "Rect coords"])
return_type_dict = {
    "Cropped image": "image",
    "Rect coords": "box"
}
return_type = return_type_dict[return_type_choice]
#intl_message = '<p style="font-family:Source Sans Pro; color:Red; font-size: 12px;">Intl Bhaktiferi only applicable from North America but excluding to India.</p>'
#st.markdown(intl_message, unsafe_allow_html=True)

# col1, col2 = st.columns(2)
# with col1:
#     intl_from = st.selectbox('International Bhaktiferi From', options=[''] + [str(year) for year in range(2024, 1980, -1)], index=0, help="from N.A. excluding to India")
# with col2:
#     intl_to = st.selectbox('International Bhaktiferi To', options=[''] + [str(year) for year in range(2024, 1980, -1)], index=0)
# if intl_from:
#         input_data[field_key] = f"{intl_from} to {intl_to}"
col1,col2 = st.columns([1,2])
col1.title('Sum:')

with st.form('addition'):
    a = st.number_input('a')
    b = st.number_input('b')
    submit = st.form_submit_button('add')

if submit:
    col2.title(f'{a+b:.2f}')
if img_file:
    img = Image.open(img_file)
    #st.image(img, caption="image as is")
    img = ImageOps.exif_transpose(img)
    ext = os.path.splitext(img_file.name)[-1].lower()
    fn = os.path.splitext(img_file.name)[0]
    st.write(ext)
    st.write(fn)
    if ext == ".png":
        st.write("This is a png file")
        img = img.convert("RGB")
        img = os.path.splitext(img_file.name)[0] + ".jpg"
        st.write("after convert")
        st.write(img)
    #st.image(img, caption="image with exif off")
    if not realtime_update:
        st.write("Double click to save crop")
    if return_type == 'box':
        rect = st_cropper(
            img,
            realtime_update=realtime_update,
            box_color=box_color,
            aspect_ratio=aspect_ratio,
            return_type=return_type,
            stroke_width=stroke_width
        )
        raw_image = np.asarray(img).astype('uint8')
        left, top, width, height = tuple(map(int, rect.values()))
        st.write(rect)
        masked_image = np.zeros(raw_image.shape, dtype='uint8')
        masked_image[top:top + height, left:left + width] = raw_image[top:top + height, left:left + width]
        st.image(Image.fromarray(masked_image), caption='masked image')
    else:
        # Get a cropped image from the frontend
        cropped_img = st_cropper(
            img,
            realtime_update=realtime_update,
            box_color=box_color,
            aspect_ratio=aspect_ratio,
            return_type=return_type,
            stroke_width=stroke_width
        )

        # Manipulate cropped image at will
        st.write(":exclamation:Preview:exclamation:")
        _ = cropped_img.thumbnail((150, 150))
        st.image(cropped_img)
        if cropped_img is not None:
            if st.button("Remove Background"):
                # Convert the input image to a numpy array
                input_array = np.array(cropped_img)
                # Apply background removal using rembg
                output_array = rembg.remove(input_array)
                # Create a PIL Image from the output array
                output_image = Image.fromarray(output_array)
                st.image(output_image, caption='Image that will be submitted', width=300)
                image = output_image   
