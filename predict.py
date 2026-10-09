from cog import BasePredictor, Input, Path
import os
from typing import List
from audio_separator.separator import Separator

class Predictor(BasePredictor):
    def setup(self):
        """آماده‌سازی اولیه پوشه‌ها در حافظه سرور"""
        self.output_dir = "/tmp/separated"
        os.makedirs(self.output_dir, exist_ok=True)

    def predict(
        self,
        audio: Path = Input(description="فایل موزیک ورودی (MP3 / WAV)")
    ) -> List[Path]:
        """پردازش اصلی و تفکیک صدا با مدل BS-RoFormer"""
        
        # تنظیم ابزار جداکننده صوتی
        separator = Separator(
            output_dir=self.output_dir,
            output_format="WAV"
        )

        # دانلود و بارگذاری مستقیم مدل استودیویی BS-RoFormer
        separator.load_model('model_bs_roformer_ep_317_sdr_12.9755.ckpt')

        # اجرای عملیات تفکیک
        output_files = separator.separate(str(audio))

        vocals_path = None
        instrumental_path = None

        for file in output_files:
            full_path = os.path.join(self.output_dir, file)
            if "Vocals" in file or "vocal" in file.lower():
                vocals_path = full_path
            else:
                instrumental_path = full_path

        # خروجی دو فایل: [آهنگ بی‌کلام, صدای خواننده]
        results = []
        if instrumental_path:
            results.append(Path(instrumental_path))
        if vocals_path:
            results.append(Path(vocals_path))

        return results
