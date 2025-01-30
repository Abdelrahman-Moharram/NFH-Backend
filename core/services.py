


def generate_unique_error_message(lang, ar_name, name, ) -> str:
    if lang == 'ar':
        return f'{ar_name} يجب ألا تتكرر'
    
    return f'this {name} already exists'