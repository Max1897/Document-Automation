from synthetic_data_generator import Synth_generator


#Generate 
generate_num = 250
file_prefix = "SYN_CADL_IS_"
file_type = ".jpg"
Output_path = "Synthetic data generation/Synthetic data/DL/CA/"
for i in range(generate_num):
    file_name = file_prefix + str(i) + file_type
    Synth_generator(Output_path + file_name)