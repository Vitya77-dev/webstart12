from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/pdf'
OUT.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('Russian','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('RussianBold','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Russian',normal='Russian',bold='RussianBold')
INK=HexColor('#0a0a0a'); MID=HexColor('#5b5b60'); HOT=HexColor('#e0431a'); BG=HexColor('#f6f4ee'); LINE=HexColor('#dad7cd')
W,H=595.28,841.89
normal=ParagraphStyle('body',fontName='Russian',fontSize=10,leading=14,textColor=INK,spaceAfter=8)
small=ParagraphStyle('small',parent=normal,fontSize=9,leading=13)
titleStyle=ParagraphStyle('title',parent=normal,fontName='RussianBold',fontSize=29,leading=35)

class Doc:
 def __init__(self,name,title,num):
  self.path=OUT/name; self.c=canvas.Canvas(str(self.path),pagesize=(W,H));self.c.setTitle(title+' | APEX');self.c.setAuthor('APEX');self.title=title;self.num=num;self.page=0;self.new_page()
 def new_page(self):
  if self.page:self.footer();self.c.showPage()
  self.page+=1;self.c.setFillColor(BG);self.c.rect(0,0,W,H,fill=1,stroke=0)
  self.c.setFillColor(HOT);self.c.rect(42,H-58,12,12,fill=1,stroke=0)
  self.c.setFillColor(INK);self.c.setFont('RussianBold',13);self.c.drawString(64,H-56,'APEX')
  self.c.setFillColor(MID);self.c.setFont('Russian',9);self.c.drawRightString(W-42,H-54,f'МАТЕРИАЛЫ ПРОГРАММЫ / {self.num:02}')
  self.c.setStrokeColor(LINE);self.c.line(42,H-73,W-42,H-73)
  self.y=H-102
  self.para(self.title,titleStyle)
  self.para('Осанка, сон и привычки. Материалы для самостоятельных записей.',small)
  self.y-=12
 def footer(self):
  self.c.setStrokeColor(LINE);self.c.line(42,57,W-42,57)
  self.c.setFont('Russian',8);self.c.setFillColor(MID);self.c.drawString(42,40,'APEX / Осанка, сон и привычки');self.c.drawRightString(W-42,40,str(self.page))
 def para(self,text,style=normal):
  p=Paragraph(text,style);_,h=p.wrap(W-84,700)
  if self.y-h<80:self.new_page()
  p.drawOn(self.c,42,self.y-h);self.y-=h+8
 def heading(self,text):
  self.y-=5;self.para(text,ParagraphStyle('h',parent=normal,fontName='RussianBold',fontSize=14,leading=18,textColor=HOT))
 def lines(self,label,count=2):
  self.para(label)
  for _ in range(count):
   self.c.setStrokeColor(LINE);self.c.line(42,self.y-12,W-42,self.y-12);self.y-=29
  self.y-=8
 def table(self,headers,rows,widths,row_height=32):
  data=[[Paragraph(str(x),small) for x in headers]]+[[Paragraph(str(x),small) for x in row] for row in rows]
  t=Table(data,colWidths=widths,rowHeights=[37]+[row_height]*len(rows))
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#ffe14a')),('GRID',(0,0),(-1,-1),.5,LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8)]))
  _,height=t.wrap(W-84,700)
  if self.y-height<80:self.new_page()
  t.drawOn(self.c,42,self.y-height);self.y-=height+20
 def save(self):self.footer();self.c.save();print(self.path.name,self.page,'pages')

d=Doc('apex-program.pdf','Программа на 12 недель',1)
d.para('Не нужно менять всё за один день. Начните с наблюдений за осанкой, затем присмотритесь ко сну и регулярности занятий. Четыре этапа помогут разложить задачи по полочкам и понять, какие привычки вам подходят.')
for title,text in [
 ('01 / Недели 1-4: присмотритесь к осанке','Запишите, что хотите изменить. Замечайте, как сидите за столом, стоите и смотрите в телефон. Если измеряете рост, отмечайте время и условия, чтобы записи можно было сравнивать.'),
 ('02 / Недели 5-8: разберитесь со сном','Записывайте время сна и самочувствие после пробуждения. Отмечайте вечерние привычки. Если появились вопросы о питании или добавках, внесите их в памятку для консультации.'),
 ('03 / Недели 9-11: найдите свой ритм','Отмечайте занятия и самочувствие. Сравнивайте план с тем, что действительно получилось. Если какая-то задача постоянно откладывается, подумайте, как сделать её удобнее.'),
 ('04 / Неделя 12: подведите итоги','Вернитесь к первым записям. Что стало привычным? Что оказалось неудобным? Выберите то, что хотите продолжить, и запишите следующий небольшой шаг.')]:d.heading(title);d.para(text)
d.para('Программа не обещает прибавку роста. Если есть боль, травмы или ограничения по нагрузке, обсудите занятия с врачом.',small)
d.new_page();d.heading('Мой план');d.lines('Что я хочу изменить:',3);d.lines('Что и в каких условиях буду записывать:',3);d.lines('За какими привычками хочу следить:',3);d.lines('Что хочу спросить у специалиста:',3);d.save()

d=Doc('nutrition-notes.pdf','Питание и добавки',2)
d.para('Когда хочется изменить питание, легко запутаться в чужих советах. Сначала запишите свой обычный режим и вопросы, которые вас волнуют. С этой памяткой будет проще подготовиться к консультации.')
d.heading('Что записать до обсуждения')
d.para('Как обычно проходит ваш день: когда едите, что выбираете и какие добавки уже принимаете. Отдельно отметьте, чего хотите добиться и что вызывает сомнения.')
d.table(['Тема','Моя запись'],[['Режим питания',''],['Вопросы о рационе',''],['Добавки, о которых хочу спросить',''],['Цель консультации','']],[160,351],36)
d.heading('Вопросы специалисту')
d.para('Есть ли основания менять рацион? Нужны ли обследования? Есть ли показания к конкретной добавке? Какие ограничения и взаимодействия необходимо учитывать?')
d.lines('Мои дополнительные вопросы:',2)
d.para('Эта памятка помогает собрать вопросы, но не назначает добавки и дозировки.',small);d.save()

d=Doc('visual-guide.pdf','Осанка и внешний вид',3)
d.para('Положение тела, одежда и обувь меняют общее впечатление. Этот лист поможет сравнить образы и выбрать то, в чём вам удобно. По фотографии нельзя точно судить об изменении роста.')
d.heading('01 / Сравнивайте в одинаковых условиях')
d.para('Если делаете фотографии, сохраняйте ракурс, расстояние, освещение и положение камеры. Изменение перспективы легко принять за изменение пропорций.')
d.heading('02 / Отмечайте детали образа')
d.para('Запишите посадку одежды, длину вещей, сочетание цветов и выбранную обувь. Оценивайте удобство и собственные предпочтения. «Правильного» роста или обязательного образа в этом упражнении нет.')
d.heading('03 / Разделяйте наблюдение и вывод')
d.para('Запишите, что именно изменилось: положение плеч, посадка одежды или ракурс. Так будет легче понять, что вам понравилось и стоит ли это повторить.')
d.table(['Параметр','Образ А','Образ Б'],[['Одежда','',''],['Обувь','',''],['Удобство','',''],['Что визуально изменилось','','']],[151,180,180],42)
d.lines('Что я выберу и почему:',2);d.save()

d=Doc('sleep-journal.pdf','Дневник сна',4)
d.para('Заполняйте одну строку после пробуждения. Отмечайте время сна и самочувствие без оценок «хорошо» или «плохо». Через неделю посмотрите, что повторяется и что хочется изменить.')
d.heading('Наблюдения за неделю')
d.table(['День','Время сна','Время подъёма','Самочувствие / заметка'],[[x,'','',''] for x in ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']],[91,86,94,240],34)
d.heading('Вечерние привычки')
d.lines('Что было перед сном и что хотелось бы отметить:',2)
d.lines('Что повторялось в течение недели:',2)
d.para('Если пропустили день, просто продолжите со следующей строки. Не нужно восстанавливать записи по памяти.',small);d.save()

d=Doc('daily-checklist.pdf','Ежедневный чек-лист',5)
d.para('Дата: ____________________    Неделя: ____________________')
d.para('Короткий список поможет не держать всё в голове. Отмечайте только то, что действительно сделали. Если что-то пропустили, продолжите в следующий день.')
d.table(['Отметка','Действие'],[['','Записать время сна и пробуждения.'],['','Отметить вечерние привычки и качество отдыха.'],['','Записать наблюдения об осанке и рабочем месте.'],['','Отметить выбранную активность и её длительность.'],['','Записать вопросы о питании или восстановлении.'],['','Внести заметку в трекер текущей недели.']],[65,446],36)
d.heading('Итог дня')
d.lines('Что удалось:',2);d.lines('Что хочу изменить или уточнить:',2)
d.para('Этот список организует наблюдения и не назначает упражнения, нагрузки или добавки.',small);d.save()

d=Doc('progress-tracker.pdf','Трекер на 12 недель',6)
d.para('Начало наблюдений: ____________________')
d.para('Заполняйте строку раз в неделю. Если измеряете рост, делайте это в одинаковых условиях и записывайте значение в сантиметрах. Отмечайте не только цифры, но и привычки, которые удалось сохранить.')
d.table(['Неделя','Дата / время','Рост','Что получилось / заметка'],[[str(n),'','',''] for n in range(1,13)],[48,112,75,276],27)
d.lines('Условия измерения:',2)
d.para('Сравнивайте свои записи между собой. Результат калькулятора не задаёт цель, которой нужно достичь.',small)
d.new_page();d.heading('Итоги наблюдений');d.lines('Какие привычки сохранились:',3);d.lines('Что мешало регулярности:',3);d.lines('Какие различия могут объясняться условиями измерения:',3);d.lines('Что хочу обсудить или уточнить дальше:',3);d.save()

with ZipFile(OUT/'apex-materials.zip','w',ZIP_DEFLATED) as archive:
 for file in sorted(OUT.glob('*.pdf')):archive.write(file,file.name)
print('ZIP created with 6 PDFs')
