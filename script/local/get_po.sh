xgettext --language=Python --from-code=utf-8 --keyword=_:1,2 -d yunsuan  ../../templates/*/*.html ../../templates/*/*/*.html

cp yunsuan_zh.po old_zh.po
cp yunsuan_zh.po bak_zh.po

cp yunsuan_en.po old_en.po
cp yunsuan_en.po bak_en.po

msgmerge  old_zh.po yunsuan.po  > yunsuan_zh.po
msgmerge  old_en.po yunsuan.po  > yunsuan_en.po

rm -f old_en.po old_zh.po  yunsuan.po

msgfmt yunsuan_en.po -o ../../locale/en_US/LC_MESSAGES/yunsuan.mo
msgfmt yunsuan_zh.po -o ../../locale/zh_CN/LC_MESSAGES/yunsuan.mo

