import cv2
import json
from faker import Faker
import matplotlib.pyplot as plt


def add_text_to_image(image, text, position, font_color, font_size, thickness):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(
        image, text, position, font, font_size, font_color, thickness, cv2.LINE_AA
    )
    return image


# output_path = file location + file name(e.g. SYN_CADL_0) + jpg
def Synth_generator(
    output_path,
    layout_path="Synthetic data generation/template/CADL.JSON",
    template_path="Synthetic data generation/template/DLTP CA Front.jpg",
    show_pic=False,
):
    # layout_path = "Synthetic data generation/template/CADL.JSON"
    # template_path = "Synthetic data generation/template/DLTP CA Front.jpg"

    with open(layout_path) as json_file:
        temp = json.load(json_file)

    image = cv2.imread(template_path)

    # Insert randomly generated text
    fake = Faker()
    for x in temp.keys():

        if x == "DL":
            temp[x]["text"] = fake.pystr_format(
                "?#######", "IOS"
            )
        elif x == "EXP":
            temp[x]["text"] = fake.pystr_format("##/##/####")
        elif x == "last_name":
            temp[x]["text"] = fake.last_name()
        elif x == "first_name":
            temp[x]["text"] = fake.first_name()
        elif x == "Address1":
            temp[x]["text"] = fake.address().split("\n")[0]
        elif x == "Address2":
            temp[x]["text"] = fake.address().split("\n")[1]
        elif x == "DOB":
            temp[x]["text"] = fake.pystr_format("##/##/####")
        elif x == "ISS":
            temp[x]["text"] = fake.pystr_format("##/##/####")

    # Put text onto template
    for subject, content in temp.items():
        modified_image = add_text_to_image(
            image,
            content["text"],
            content["POS"],
            content["font_color"],
            content["font_size"],
            content["thickness"],
        )

    # Convert BGR image to RGB (for displaying with Matplotlib)
    modified_image_rgb = cv2.cvtColor(modified_image, cv2.COLOR_BGR2RGB)

    # Plot the modified image
    plt.imshow(modified_image_rgb)
    plt.axis("off")
    plt.savefig(output_path)
    if show_pic:
        plt.show()
