# توقيت الإنتاج

قبل استلام صوت المستخدم من Google AI Studio، سلّم جدولًا مستقلًا ببداية ونهاية مستهدفتين لكل مقطع بصيغة MM:SS، مع السكريبت المنطوق ونص إرشادات الأداء منفصلًا عنه. هذه تقديرات تخطيطية وليست محاذاة للصوت. انتظر الملف الذي ينشئه المستخدم؛ لا تنشئ timeline.json نهائيًا ولا تبدأ تصدير MP4 قبله.
بعد استلام الملف، اكتب JSON بالقيم الفعلية المشتقة من الصوت، ثم أدخل صمت التفكير وحدّث الأزمنة. المسارات نسبة إلى مجلد ملف JSON والمدد بالثواني.

```json
{
  "width": 1280,
  "height": 720,
  "fps": 30,
  "duration": 60.0,
  "audio": "voice-final.wav",
  "font_regular": "assets/Cairo-Regular.ttf",
  "font_bold": "assets/Cairo-Bold.ttf",
  "scenes": [
    {"id":"hook","start":0,"end":5,"text":"سؤال افتتاحي","motion":"title-reveal","purpose":"استدعاء المعرفة"},
    {"id":"explain","start":5,"end":50,"text":"نصوص مختصرة","motion":"meaningful-steps","purpose":"شرح المفهوم"},
    {"id":"question","start":50,"end":60,"text":"سؤال استرجاع","motion":"question-then-answer","purpose":"قياس الفهم"}
  ],
  "question":{"prompt_end":53,"answer_start":58,"answer_end":60}
}
```

هذه بنية لا خطة ثابتة
قسّم explain إلى مشاهد فعلية لكل فكرة بدل إبقائه 45 ثانية
غطِّ مدة الفيديو بالكامل دون فجوات أو تداخل مشاهد
يجوز تداخل عناصر داخل المشهد نفسه
احتفظ بدليل توقيتات الصوت من المزود أو الاستماع أو المحاذاة
الفحص البرمجي لا يثبت الدقة العلمية أو جودة النطق والحركة

Choose width and height from the requested orientation before rendering
Use 1920×1080 or 1280×720 for landscape 16:9 and 1080×1920 or 720×1280 for portrait 9:16
Recompose portrait scenes instead of cropping or stretching landscape frames
