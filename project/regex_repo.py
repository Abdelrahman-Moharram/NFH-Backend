phone_number_pattern        = '^[0-9]{8}$'
identity_number_pattern     = '^[1-9][0-9]{9}$'
hijri_date_pattern          = '^([٠-٢]?[٠-٩])-([٠-١]?[٠-٩])-(١[٣-٤][٠-٩][٠-٩]|[١٢][٠-٩][٠-٩][٠-٩])$'
amount_pattern               = '^[0-9.]+$'
username_pattern            = '^[a-zA-Z][a-zA-Z0-9_. -]{2,}$'
ar_name_pattern             = '^[ء-ي][ء-ي ]{5,}$'
email_pattern               = '^[a-z][a-z0-9-_\.]+@[a-z.]+\.[a-z]{2,3}$'


username_regex           = {'pattern':username_pattern,         'message':'اسم المستخدم يجب ان يبدأ بأحرف ويحتوي على 3 أحرف على الأقل ولا يحتوي على [+%$#/|\\!]'}
ar_name_regex            = {'pattern':ar_name_pattern,          'message':'اسم المستخدم باللغة العربية يجب ان يكون كاملا باللغة العربية و بدون ارقام ولا يقل عن 5 أحرف'}
phone_number_regex       = {'pattern':phone_number_pattern,     'message':'يجب أن يحتوي يبدأ رقم الجوال على 8 ارقام بعد (9665+)'}
amount_regex             = {'pattern':amount_pattern,           'message':'يجب أن يحتوي الملبغ على أرقام فقط'}
identity_number_regex    = {'pattern':identity_number_pattern,  'message':'رقم الهوية يجب أن يحوي على 10 أرقام ولا يبدأ ب "0"'}
email_regex              = {'pattern':email_pattern,            'message':'البريد الإلكتروني غير صالح "example@domain.com" '}