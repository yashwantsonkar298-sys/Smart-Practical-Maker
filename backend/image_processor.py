import textwrap
import random
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

class EliteDocumentEngine:
    def __init__(self):
        self.tool_configs = {
            'blue': {'colors': [(10, 24, 115), (15, 32, 128), (5, 15, 90)], 'opacity': (235, 255)},
            'black': {'colors': [(20, 25, 30), (10, 15, 20), (32, 38, 50)], 'opacity': (240, 255)},
            'pencil': {'colors': [(85, 90, 100), (70, 75, 85)], 'opacity': (140, 190)}
        }

    def _apply_stealth_filters(self, image, req):
        if req.stealth_scanner_effect:
            img_arr = np.array(image)
            noise = np.random.randint(-12, 12, img_arr.shape, dtype='int16')
            noisy_img = np.clip(img_arr + noise, 0, 255).astype('uint8')
            image = Image.fromarray(noisy_img)
        if req.uneven_lighting:
            shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
            sdraw = ImageDraw.Draw(shadow)
            sdraw.rectangle([0, 0, image.width, 150], fill=(0, 0, 0, 20))
            sdraw.rectangle([0, image.height-200, image.width, image.height], fill=(0, 0, 0, 25))
            shadow = shadow.filter(ImageFilter.GaussianBlur(60))
            image = Image.alpha_composite(image.convert("RGBA"), shadow)
        return image

    def _draw_paper(self, style, width, height, line_gap, margin_left):
        paper = Image.new("RGBA", (width, height), (252, 251, 248, 255))
        draw = ImageDraw.Draw(paper)
        if style == 'ruled':
            draw.line([(margin_left - 15, 0), (margin_left - 15, height)], fill=(230, 90, 90, 150), width=3)
            for y in range(180, height - 80, line_gap):
                draw.line([(0, y), (width, y)], fill=(170, 190, 230, 120), width=2)
        return paper

    def compile_document(self, req, font_path, page_style) -> list:
        width, height = 1240, 1754 
        font_size = req.font_size
        line_gap = req.line_gap
        margin_left = req.margin_left
        start_y = req.top_margin # 🎯 USED TOP MARGIN HERE
        
        font = ImageFont.truetype(font_path, font_size)
        compiled_pages = []
        page_num = 1
        current_y = start_y
        
        paragraphs = req.text.split('\n')
        
        bg = self._draw_paper(page_style, width, height, line_gap, margin_left)
        text_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)

        # 🎯 CUSTOM HEADER POSITION USED HERE
        if req.lab_header:
            header_font = ImageFont.truetype(font_path, int(font_size * 0.9))
            draw.text((req.header_x, req.header_y), f"Name: {req.student_name} | Roll: {req.roll_number}", font=header_font, fill=(30, 30, 90, 200))
            draw.text((width - 350, req.header_y), f"Date: {req.date}", font=header_font, fill=(30, 30, 90, 200))

        for block in paragraphs:
            if not block.strip():
                current_y += line_gap
                continue

            max_chars = int((width - margin_left - 100) / (font.getlength("a") * 1.4))
            lines = textwrap.wrap(block, width=max_chars)

            for line in lines:
                if current_y >= (height - 150):
                    if req.page_numbering:
                        draw.text((width//2, height-80), f"- {page_num} -", font=font, fill=(50, 50, 50, 150))
                    
                    if req.ink_smudge_level > 0:
                        text_layer = text_layer.filter(ImageFilter.GaussianBlur(req.ink_smudge_level * 0.3))
                    
                    final = Image.alpha_composite(bg, text_layer)
                    final = self._apply_stealth_filters(final, req)
                    
                    buf = io.BytesIO()
                    final.save(buf, format='PNG')
                    compiled_pages.append(buf.getvalue())
                    
                    page_num += 1
                    current_y = start_y
                    bg = self._draw_paper(page_style, width, height, line_gap, margin_left)
                    text_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
                    draw = ImageDraw.Draw(text_layer)

                curr_x = margin_left + random.randint(-2, 2)
                for word in line.split(' '):
                    if not word: 
                        curr_x += font.getlength(" ")
                        continue
                    
                    sx, sy, color = self._get_ink(req.ink_color, req.realism_factor)
                    draw.text((curr_x + sx, current_y + sy), word, font=font, fill=color)
                    
                    w_width = font.getbbox(word)[2] - font.getbbox(word)[0]
                    curr_x += w_width + font.getlength(" ") + random.randint(0, req.realism_factor)
                
                current_y += line_gap

        if req.page_numbering:
            draw.text((width//2, height-80), f"- {page_num} -", font=font, fill=(50, 50, 50, 150))
        if req.ink_smudge_level > 0:
            text_layer = text_layer.filter(ImageFilter.GaussianBlur(req.ink_smudge_level * 0.3))
        
        final = Image.alpha_composite(bg, text_layer)
        final = self._apply_stealth_filters(final, req)
        buf = io.BytesIO()
        final.save(buf, format='PNG')
        compiled_pages.append(buf.getvalue())

        return compiled_pages

    def _get_ink(self, ink_type, realism):
        conf = self.tool_configs.get(ink_type, self.tool_configs['blue'])
        color = random.choice(conf['colors'])
        alpha = random.randint(*conf['opacity'])
        return random.randint(-realism, realism), random.randint(-realism, realism), color + (alpha,)

processor = EliteDocumentEngine()