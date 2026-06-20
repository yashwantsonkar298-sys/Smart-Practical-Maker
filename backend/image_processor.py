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

    def _print_font(self, size, italic=False):
        candidates = [
            "C:/Windows/Fonts/ariali.ttf" if italic else "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibrii.ttf" if italic else "C:/Windows/Fonts/calibri.ttf",
            "DejaVuSans-Oblique.ttf" if italic else "DejaVuSans.ttf",
            "arial.ttf",
        ]
        for font_name in candidates:
            try:
                return ImageFont.truetype(font_name, size)
            except OSError:
                continue
        return ImageFont.load_default()

    def _dotted_line(self, draw, x1, y, x2, fill, dot=3, gap=7):
        x = x1
        while x < x2:
            draw.line([(x, y), (min(x + dot, x2), y)], fill=fill, width=2)
            x += dot + gap

    def _draw_grid_paper(self, draw, width, height):
        grid_fill = (175, 200, 230, 85)
        for x in range(0, width, 40):
            draw.line([(x, 0), (x, height)], fill=grid_fill, width=1)
        for y in range(0, height, 40):
            draw.line([(0, y), (width, y)], fill=grid_fill, width=1)

    def _break_long_word(self, word, font, max_width):
        parts = []
        current = ""
        for char in word:
            candidate = current + char
            if current and font.getlength(candidate) > max_width:
                parts.append(current)
                current = char
            else:
                current = candidate
        if current:
            parts.append(current)
        return parts or [word]

    def _wrap_text_to_width(self, text, font, max_width, realism):
        words = text.split(" ")
        lines = []
        current_words = []
        current_width = 0
        space_width = font.getlength(" ") + max(0, realism)

        for word in words:
            if word == "":
                continue

            word_width = font.getlength(word)
            if word_width > max_width:
                parts = self._break_long_word(word, font, max_width)
            else:
                parts = [word]

            for part in parts:
                part_width = font.getlength(part)
                next_width = part_width if not current_words else current_width + space_width + part_width
                if current_words and next_width > max_width:
                    lines.append(" ".join(current_words))
                    current_words = [part]
                    current_width = part_width
                else:
                    current_words.append(part)
                    current_width = next_width

        if current_words:
            lines.append(" ".join(current_words))
        return lines

    def _draw_abes_practical_sheet(self, paper, line_gap):
        width, height = paper.size
        draw = ImageDraw.Draw(paper)
        print_fill = (38, 45, 48, 235)
        line_fill = (28, 55, 58, 190)
        faint_fill = (38, 58, 62, 150)
        x_margin = 90
        right_edge = width - 48
        header_font = self._print_font(24)
        footer_font = self._print_font(28)
        signature_font = self._print_font(24, italic=True)

        for y in range(76, height - 58, 24):
            draw.line([(x_margin, y), (x_margin, y + 9)], fill=line_fill, width=3)

        for y in range(184, height - 170, line_gap):
            draw.line([(x_margin + 8, y), (right_edge, y)], fill=faint_fill, width=2)

        draw.text((646, 92), "Roll No.:", font=header_font, fill=print_fill)
        self._dotted_line(draw, 754, 114, 846, print_fill)
        draw.text((865, 92), "Date", font=header_font, fill=print_fill)
        self._dotted_line(draw, 926, 114, 1008, print_fill)
        draw.text((1028, 92), "Page No.", font=header_font, fill=print_fill)
        self._dotted_line(draw, 1136, 114, 1210, print_fill)

        draw.text((126, 138), "Practical Name:", font=header_font, fill=print_fill)
        self._dotted_line(draw, 316, 160, 930, print_fill)
        draw.text((930, 138), "Practical No.", font=header_font, fill=print_fill)
        self._dotted_line(draw, 1082, 160, 1210, print_fill)

        hole_specs = [
            (x_margin - 4, 600, 18, (42, 52, 55, 245)),
            (x_margin - 8, 655, 14, (52, 62, 58, 225)),
            (x_margin - 8, 1110, 18, (44, 54, 57, 245)),
            (x_margin - 10, 1148, 16, (32, 43, 46, 245)),
        ]
        for cx, cy, radius, fill in hole_specs:
            draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=fill)
            draw.ellipse(
                [cx - radius + 5, cy - radius + 5, cx + radius - 5, cy + radius - 5],
                fill=(20, 25, 28, 210),
            )

        mesh_cx, mesh_cy, mesh_radius = x_margin - 8, 655, 14
        for offset in range(-mesh_radius, mesh_radius + 1, 7):
            mesh_y = mesh_cy + offset
            draw.line(
                [(mesh_cx - mesh_radius, mesh_y), (mesh_cx + mesh_radius, mesh_y)],
                fill=(198, 206, 190, 160),
                width=1,
            )
            mesh_x = mesh_cx + offset
            draw.line(
                [(mesh_x, mesh_cy - mesh_radius), (mesh_x, mesh_cy + mesh_radius)],
                fill=(198, 206, 190, 160),
                width=1,
            )

        draw.text((148, height - 104), "ABES Engineering College", font=footer_font, fill=print_fill)
        draw.text((922, height - 102), "Sign of Faculty with Date", font=signature_font, fill=print_fill)

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
        if style == 'abes_practical':
            self._draw_abes_practical_sheet(paper, line_gap)
        elif style == 'grid':
            self._draw_grid_paper(draw, width, height)
        elif style == 'ruled':
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
        if req.lab_header and page_style != 'abes_practical':
            header_font = ImageFont.truetype(font_path, int(font_size * 0.9))
            header_line_gap = int(font_size * 0.9) + 10
            school_bits = []
            if req.college_name:
                school_bits.append(f"College: {req.college_name}")
            if req.subject_code:
                school_bits.append(f"Subject: {req.subject_code}")
            if school_bits:
                draw.text((req.header_x, req.header_y), " | ".join(school_bits), font=header_font, fill=(30, 30, 90, 200))
            meta_y = req.header_y + header_line_gap if school_bits else req.header_y
            draw.text((req.header_x, meta_y), f"Name: {req.student_name} | Roll: {req.roll_number}", font=header_font, fill=(30, 30, 90, 200))
            draw.text((width - 350, meta_y), f"Date: {req.date}", font=header_font, fill=(30, 30, 90, 200))

        for block in paragraphs:
            if not block.strip():
                current_y += line_gap
                continue

            right_margin = margin_left
            max_line_width = width - margin_left - right_margin
            lines = self._wrap_text_to_width(block, font, max_line_width, req.realism_factor)

            for line in lines:
                if current_y >= (height - 150):
                    if req.page_numbering and page_style != 'abes_practical':
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

        if req.page_numbering and page_style != 'abes_practical':
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
