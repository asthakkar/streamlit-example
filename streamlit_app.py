import streamlit as st
import numpy as np
from streamlit_cropper import st_cropper
from PIL import Image
from PIL import ImageOps
import rembg
import os
from streamlit_extras.let_it_rain import rain
import leafmap.foliumap as leafmap

#if st.secrets["maintenance_mode"] == "TRUE":
#    st.write ("The Site is in Maintenance Mode.  Please check back again later.")
#    st.stop()

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.title("Swadhyaya Kendra Locations")
m = leafmap.Map(center=[40, -100], zoom=2)
cities = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
regions = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson"

m.add_geojson(regions, layer_name="US Regions")
m.add_points_from_xy(
    cities,
    x="longitude",
    y="latitude",
    color_column="region",
    icon_names=["gear", "map", "leaf", "globe"],
    spin=True,
    add_legend=True,
)

m.to_streamlit(height=700)

# st.set_option('deprecation.showfileUploaderEncoding', False)
# # Upload an image and set some options for demo purposes
# st.header("Test App")
# img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])
# realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
# box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
# stroke_width = st.sidebar.number_input(label="Box Thickness", value=3, step=1)

# aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
# aspect_dict = {
#     "1:1": (1, 1),
#     "16:9": (16, 9),
#     "4:3": (4, 3),
#     "2:3": (2, 3),
#     "Free": None
# }
# aspect_ratio = aspect_dict[aspect_choice]

# return_type_choice = st.sidebar.radio(label="Return type", options=["Cropped image", "Rect coords"])
# return_type_dict = {
#     "Cropped image": "image",
#     "Rect coords": "box"
# }
# return_type = return_type_dict[return_type_choice]
# #intl_message = '<p style="font-family:Source Sans Pro; color:Red; font-size: 12px;">Intl Bhaktiferi only applicable from North America but excluding to India.</p>'
# #st.markdown(intl_message, unsafe_allow_html=True)

# # col1, col2 = st.columns(2)
# # with col1:
# #     intl_from = st.selectbox('International Bhaktiferi From', options=[''] + [str(year) for year in range(2024, 1980, -1)], index=0, help="from N.A. excluding to India")
# # with col2:
# #     intl_to = st.selectbox('International Bhaktiferi To', options=[''] + [str(year) for year in range(2024, 1980, -1)], index=0)
# # if intl_from:
# #         input_data[field_key] = f"{intl_from} to {intl_to}"


# def example():
#     rain(
#         emoji="🍂",
#         font_size=54,
#         falling_speed=5,
#         animation_length="2",
#     )
# # Camera input
# #image = st.camera_input("Scan your QR Code")

# # option = st.selectbox(
# #     'We can do different options for successful submission.  What would you like to see?',
# #     (' ', 'Balloons', 'Snow', 'Toast', 'Leaves'))

# #st.write('You selected:', option)
# #submit = st.form_submit_button('Submit')

# # if option:
# #     if option == "Balloons":
# #         st.balloons()
# #     elif option == "Snow":
# #         st.snow()
# #     elif option == "Toast":
# #          st.toast('Thank you.  Your information is submitted!', icon='👍')
# #     elif option == "Leaves":
# #         example()
# #     else:
# #         st.write ("Please make a selection.")
# if img_file:
#     img = Image.open(img_file)
#     width, height = img.size
#     st.write(width)
#     st.write(height)
#     if((width < 700) or (height < 700)):
#         st.write ("image is too small")
#         st.stop()
#     #st.image(img, caption="image as is")
#     img = ImageOps.exif_transpose(img)
#     ext = os.path.splitext(img_file.name)[-1].lower()
#     fn = os.path.splitext(img_file.name)[0]
#     st.write(ext)
#     st.write(fn)
#     if ext == ".png":
#         st.write("This is a png file")
#         img = img.convert("RGB")
#         img = os.path.splitext(img_file.name)[0] + ".jpg"
#         st.write("after convert")
#         st.write(img)
#     #st.image(img, caption="image with exif off")
#     if not realtime_update:
#         st.write("Double click to save crop")
#     if return_type == 'box':
#         rect = st_cropper(
#             img,
#             realtime_update=realtime_update,
#             box_color=box_color,
#             aspect_ratio=aspect_ratio,
#             return_type=return_type,
#             stroke_width=stroke_width
#         )
#         raw_image = np.asarray(img).astype('uint8')
#         left, top, width, height = tuple(map(int, rect.values()))
#         st.write(rect)
#         masked_image = np.zeros(raw_image.shape, dtype='uint8')
#         masked_image[top:top + height, left:left + width] = raw_image[top:top + height, left:left + width]
#         st.image(Image.fromarray(masked_image), caption='masked image')
#     else:
#         # Get a cropped image from the frontend
#         cropped_img = st_cropper(
#             img,
#             realtime_update=realtime_update,
#             box_color=box_color,
#             aspect_ratio=aspect_ratio,
#             return_type=return_type,
#             stroke_width=stroke_width
#         )

#         # Manipulate cropped image at will
#         st.write(":exclamation:Preview:exclamation:")
#         _ = cropped_img.thumbnail((150, 150))
#         st.image(cropped_img)
#         if cropped_img is not None:
#             if st.button("Remove Background"):
#                 # Convert the input image to a numpy array
#                 input_array = np.array(cropped_img)
#                 # Apply background removal using rembg
#                 output_array = rembg.remove(input_array)
#                 # Create a PIL Image from the output array
#                 output_image = Image.fromarray(output_array)
#                 st.image(output_image, caption='Image that will be submitted', width=300)
#                 image = output_image   
