import os
from AWS_Rekognition import classifier_reko

def main():
    directory = 'raw data\AWS Rekognition data'
    output = open("output.txt", "w")
    output.write("")
    output.close()

    output = open("output.txt","a")
    
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        label_name = classifier_reko(f)
        output.write(filename+" detected as : "+label_name + "\n")
    
    output.close()

    

   
        

if __name__ == "__main__":
    main()
 
