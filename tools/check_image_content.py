from PIL import Image
import io

try:
    with open('assets/favicons/7dadb4e62aa7584241decf0aa741471a.png', 'rb') as f:
        img_data = f.read()
    
    # 尝试用PIL打开图片
    img = Image.open(io.BytesIO(img_data))
    
    print(f'图片格式: {img.format}')
    print(f'图片模式: {img.mode}')
    print(f'图片尺寸: {img.size}')
    print(f'图片是否透明: {img.mode == "RGBA"}')
    
    # 检查图片是否为空或全透明
    if img.mode == 'RGBA':
        # 检查alpha通道
        alpha = img.split()[3]
        alpha_min, alpha_max = alpha.getextrema()
        print(f'Alpha通道范围: {alpha_min} - {alpha_max}')
        print(f'图片是否全透明: {alpha_max == 0}')
    
    # 检查图片是否全为一种颜色
    colors = img.getcolors()
    print(f'图片颜色数量: {len(colors) if colors else 0}')
    if colors and len(colors) == 1:
        print(f'图片只有一种颜色: {colors[0]}')
        
except Exception as e:
    print(f'打开图片失败: {e}')
    print('尝试检查文件内容...')
    
    # 检查文件内容
    with open('assets/favicons/7dadb4e62aa7584241decf0aa741471a.png', 'rb') as f:
        content = f.read()
    
    print(f'文件大小: {len(content)} 字节')
    print(f'文件头: {content[:32].hex()}')
