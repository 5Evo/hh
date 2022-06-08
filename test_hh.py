from hh_methods import skil_stat

def test_skil_stat():
    add_skil = ['Python', 'SQL', 'Diango', 'python', 'python' ]
    new_skils = skil_stat(add_skil)
    print(f'\nСловарь скилов: {new_skils}')
    assert new_skils == {'diango': 1, 'python': 3, 'sql': 1}