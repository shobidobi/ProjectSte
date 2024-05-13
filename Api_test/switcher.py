from Stenography.Image.LSBEncode import LSBEncode
from Stenography.Image.LSBDecoded import LSBDecoded
from Stenography.Image.MSBEncoded import MSBEncoded
from Stenography.Image.MSBDecoded import MSBDecoded
from Stenography.Image.PVDEncoded import PVDEncoded
from Stenography.Image.PVDDecoded import PVDDecoded
from Stenography.Audio.LSBEncodedA import LsbEncodedA
from Stenography.Audio.LSBDecodedA import LsbDecodedA
from Stenography.Audio.MSBEecodedA import MSBEecodedA
from Stenography.Audio.MSBDecodedA import MSBDecodedA
def switch_code(company_number,algorithm_type,pixel_range,file_type,mode,text,path):
    """
       Switches between different steganographic algorithms based on the parameters.

       :param company_number: The company number.
       :param algorithm_type: The type of steganographic algorithm ('LSB', 'MSB', 'PVD').
       :param pixel_range: The range of pixels for hiding the message.
       :param file_type: The type of file ('image', 'audio').
       :param mode: The mode of operation ('encode', 'decode').
       :param text: The message to be hidden.
       :param path: The path to the file.
       :return: Encoded or decoded data, and the algorithm type used.
       """
    print(algorithm_type,pixel_range,file_type,mode,text,path)
    print(path)
    if algorithm_type=='LSB':
        if file_type=='image':
            if mode=='encode':
                LSBEncode_=LSBEncode()
                return LSBEncode_.lsb(text,image_path=path,range_pixel=[pixel_range[0],pixel_range[1]]),algorithm_type
            else:
                LSBDecoded_=LSBDecoded
                return LSBDecoded_.decode(image_path=path,range_pix=[pixel_range[0],pixel_range[1]]),algorithm_type
        else:
            if mode=='encode':
                LsbEncodedA_=LsbEncodedA()
                return LsbEncodedA_.encode(audio_file=path,message=text),algorithm_type
            else:
                LsbDecodedA_=LsbDecodedA()
                return LsbDecodedA_.decode(audio=path),algorithm_type
    if algorithm_type=='MSB':
        if file_type=='image':
            if mode=='encode':
                print("dfgdgdfgdfgd")
                MSBEncoded_=MSBEncoded()
                return MSBEncoded_.encode(text,image_path=path,range_pixel=[pixel_range[0],pixel_range[1]]),algorithm_type
            else:
                MSBDecoded_=MSBDecoded()
                return MSBDecoded_.decode(image_path=path,range_pixel=[pixel_range[0],pixel_range[1]]),algorithm_type
        else:
            if mode=='encode':
                MSBEecodedA_=MSBEecodedA()
                return MSBEecodedA_.encode(audio_file=path,message=text),algorithm_type
            else:
                MSBDecodedA_=MSBDecodedA()
                return MSBDecodedA_.decode(audio=path),algorithm_type
    if algorithm_type=='PVD':
        if file_type=='image':
            if mode=='encode':
                PVDEncoded_=PVDEncoded()
                return PVDEncoded_.pvd(text,image_path=path,range_pixel=[pixel_range[0],pixel_range[1]+30]),algorithm_type
            else:
                PVDDecoded_=PVDDecoded()
                return PVDDecoded_.pvd(image_path=path),algorithm_type



