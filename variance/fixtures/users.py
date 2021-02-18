#username, email, password, birthdate, role, (flags)
TESTING_USERS=[
("test1","test1@example.com","password1","1998-07-20","user",None),
("test2","test2@example.com","password2","1998-07-20","user",None),
("test-admin","test-admin@example.com","password-admin","1960-06-11","admin",None),
("test-admin2","test-admin2@example.com","password-admin2","1960-09-02","admin",None),
("test-nonuts","nonuts@example.com","passwordNUTS","1975-10-05","user",("nopeanuts","notreenuts")),
("test-vegan","vegan@example.com","passwordVEGAN","1995-12-12","user",("vegan")),
("test-gluten","gluten@example.com","passwordGLUTEN","2000-04-19","user",("nogluten"))
]
DEFAULT_USERS=[
("admin","admin@localhost","variance-admin","2021-02-18","admin",None)
]