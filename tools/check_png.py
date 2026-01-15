with open('assets/favicons/7dadb4e62aa7584241decf0aa741471a.png', 'rb') as f:
    header = f.read(8)
    print(f'PNG header: {header}')
    print(f'PNG header bytes: {[hex(b) for b in header]}')
    expected = b'\x89PNG\r\n\x1a\n'
    print(f'Expected header: {expected}')
    print(f'Expected header bytes: {[hex(b) for b in expected]}')
    print(f'Is valid PNG: {header == expected}')
