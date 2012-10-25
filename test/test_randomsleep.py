from hardhat import randomsleep

def test_randomsleep():
    '''randomsleep shouldn't fail.'''
    randomsleep(0, 0)
    randomsleep(mean = 0, sd = 0)
