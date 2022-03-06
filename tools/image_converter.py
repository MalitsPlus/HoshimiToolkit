from msilib.schema import Error
import inference_realesrgan
import sys
import contextlib
from pathlib import Path
from PIL import Image
sys.path.append("../")
import tools.rich_console as console

# ipr inner_size = (1820, 1024)

def convert(inputs: str = "inputs", output: str = "results", scale: str = "2", tile: str = "256", extension: str = "auto"):
    """不对图像做任何预处理或后处理，直接使用ESRGAN\n
    Common usage: convert(inputs="inputPath", output="outputPath", scale="1.5")
    """
    _do_convert(inputs=inputs, output=output, scale=scale, tile=tile, extension=extension)

def convert_resize(c_size: tuple, inputs: str = "inputs", output: str = "results", scale: str = "2", tile: str = "256", extension: str = "auto"):
    """先将图片处理为指定分辨率，再以指定scale采用ESRGAN放大图片。\n
    此方法适合 (目标分辨率/原图分辨率) 较大的场景。\n
    Common usage: convert_resize(c_size=(1821, 1024), inputs="inputPath", output="outputPath", scale="1.5")
    """
    _do_convert(inputs=inputs, output=output, scale=scale, tile=tile, extension=extension, resize=True, c_size=c_size)

def convert_to_size(c_size: tuple, inputs: str = "inputs", output: str = "results", scale: str = "2", tile: str = "256", extension: str = "auto"):
    """先以指定scale采用ESRGAN放大图片，再将图片缩小为指定分辨率。\n
    此方法适合 (目标分辨率/原图分辨率) 较小的场景。\n
    Common usage: convert_resize(c_size=(1920, 1080), inputs="inputPath", output="outputPath")
    """
    _do_convert(inputs=inputs, output=output, scale=scale, tile=tile, extension=extension, to_size=True, c_size=c_size)

def _do_convert(inputs: str, output: str, scale: str, tile: str, extension: str, resize: bool=False, to_size: bool=False, c_size: tuple=(0, 0)):
    input_cache = inputs

    # Pre-convert
    if resize:
        console.info("Begin pre-converting...")
        input_dir = Path(inputs)
        input_cache = input_dir/"convert_cache"
        input_cache.mkdir(exist_ok=True)
        for img_path in input_dir.glob("*.png"):
            img = Image.open(img_path)
            img = img.resize(c_size, resample=Image.LANCZOS, reducing_gap=3)
            img.save(fp=Path(input_cache).joinpath(img_path.name), format="png")
        
    console.info("Start converting...")
    try:
        _convert_with_esrgan(inputs=str(input_cache), output=output, scale=scale, tile=tile, extension=extension)
    except Exception as err:
        console.error(err)
        raise
    finally:
        if resize:
            try:
                for img_path in input_cache.glob("*.png"):
                    img_path.unlink()
                input_cache.rmdir()
            except Exception as rmer:
                console.error(rmer)

    # Re-convert
    if to_size:
        console.info("Begin after-converting.")
        input_cache = Path(output)
        for img_path in input_cache.glob("*.png"):
            img = Image.open(img_path)
            img = img.resize(c_size, resample=Image.LANCZOS, reducing_gap=3)
            img.save(fp=img_path, format="png")

    console.succeed("Conversion completed.")

@contextlib.contextmanager
def _redirect_argv(args: list):
    arg0 = sys.argv[0]
    args.insert(0, arg0)
    sys.argv = args

def _convert_with_esrgan(inputs: str, output: str, scale: str, tile: str, extension: str):
    """Original Doc:
        Usage: python inference_realesrgan.py -n RealESRGAN_x4plus -i infile -o outfile [options]...

        A common command: python inference_realesrgan.py -n RealESRGAN_x4plus -i infile --outscale 3.5 --half --face_enhance

        -h                   show this help
        -i --input           Input image or folder. Default: inputs
        -o --output          Output folder. Default: results
        -n --model_name      Model name. Default: RealESRGAN_x4plus
        -s, --outscale       The final upsampling scale of the image. Default: 4
        --suffix             Suffix of the restored image. Default: out
        -t, --tile           Tile size, 0 for no tile during testing. Default: 0
        --face_enhance       Whether to use GFPGAN to enhance face. Default: False
        --half               Whether to use half precision during inference. Default: False
        --ext                Image extension. Options: auto | jpg | png, auto means using the same extension as inputs. Default: auto
    """
    arg_list = [
        "-n", "RealESRGAN_x4plus_anime_6B", 
        "--suffix", "esrgan", 
        "-s", scale,
        "-i", inputs,
        "-o", output,
        "--ext", extension,
        "-t", tile
    ]
    _redirect_argv(arg_list)
    inference_realesrgan.main()

if __name__ == "__main__":
    # convert_resize(
    #     c_size=(1821, 1024), 
    #     inputs=r"F:\CG\IDOLY PRIDE Extract\tmp",
    #     output=r"F:\CG\IDOLY PRIDE Extract\OutTest",
    #     scale="2", 
    #     tile="256", 
    # )
    convert_to_size(
        c_size=(2560, 1440),
        inputs=r"F:\CG\IDOLY PRIDE Extract\tmp",
        output=r"F:\CG\IDOLY PRIDE Extract\Cards",
        tile="256",
    )
