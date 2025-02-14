import psycopg2, git

connection = psycopg2.connect(database="postgres", user="postgres", password="admin", host="127.0.0.1", port=5432)

cursor = connection.cursor()

# Lista de instruções SQL para serem executadas
sql_statements = [
    """
    INSERT INTO api_activitytype (name, total_max, per_submission_max) 
    VALUES ('Cursos de língua estrangeira – mínimo três semestres', 60, 60), 
    ('Cursos de complementação de conteúdos das disciplinas do curso – mínimo 50 % da carga horária do curso', 60, 60),
    ('Cursos de formação geral: política, sociedade, ética profissional – mínimo 50 % da carga horária do curso', 60, 60),
    ('Apresentação de trabalhos na Semana Universitária – oral ou painel', 48, 8),
    ('Apresentação de trabalhos em congressos, simpósios, encontros nacionais – oral ou painel', 48, 8),
    ('Prêmio acadêmico, artístico ou cultural', 60, 15),
    ('Trabalhos completos publicados em anais', 80, 20),
    ('Publicação de livros de divulgação científica com ISBN', 80, 20),
    ('Publicação de capítulo de livros com ISBN', 50, 10),
    ('Publicação de livros na área de conhecimento do Curso – autor único ou com até 3 (três) autores', 60, 15),
    ('Publicação de Resumos em Congressos Científicos locais', 20, 2),
    ('Publicação de Resumos em Congressos Científicos regionais', 30, 3),
    ('Publicação de Resumos em Congressos Científicos nacionais', 40, 4),
    ('Publicação de Resumos em Congressos Científicos internacionais', 40, 5),
    ('Publicação de Artigos em revistas locais com corpo editorial', 50, 10),
    ('Publicação de Artigos em revistas nacionais com corpo editorial', 60, 15),
    ('Publicação de Artigos em revistas internacionais com corpo editorial', 80, 20),
    ('Publicação de Artigos de divulgação científica, tecnológica e artística em revista especializada', 20, 5),
    ('Publicação de Artigos de divulgação científica, tecnológica e artística em jornais', 20, 5),
    ('Participação em eventos: congressos, semanas, encontros, oficinas, palestras, conferências, mesas-redondas, seminários, simpósios, desde que observe o que preceitua o Art. 2º da Resolução Nº 3241', 40, 2),
    ('Participação em comissões organizadoras de eventos acadêmicos, artísticos e culturais com duração mínima de 20 horas', 40, 10),
    ('Catalogação de documentos em Instituições parceiras aprovadas pelo colegiado do curso', 20, 20),
    ('Produção de material didático com orientação de Coordenadores da UECE', 40, 8),
    ('Participação em campanhas de saúde pública: vacinação, prevenção de epidemias', 20, 5),
    ('Participação em campanhas e atividades de educação ambiental', 20, 5),
    ('Produção de filmes, vídeos ou audiovisuais de informação científicos e culturais', 20, 5),
    ('Direção de peça, vídeo e audiovisual de produção artística', 20, 5),
    ('Mostras de artes plásticas', 20, 5),
    ('Composição musical', 20, 5),
    ('Participação em grupo artístico da UECE', 15, 3),
    ('Curso de informática – mínimo 50 % da carga horária do curso', 60, 60);
    """,
    """
    INSERT INTO api_major (name) 
    VALUES ('Psychology'), ('Computer Science');
    """,
    """
    INSERT INTO api_principal (email, enrollment_number, name, password, picture, "majorId_id") 
    VALUES 
    ('beloved@uece.br', '001', 'Mathew Paixas', '14151617', 'files/images/principal/malone.png', 2),
    ('o_freudianinho@uece.br', '002', 'Sigmund Freud', 'nome_da_mae_do_freud', 'files/images/principal/freud.png', 1);
    """,
    """
    INSERT INTO api_professor (email, enrollment_number, status, name, password, picture, "majorId_id")
    VALUES 
    ('the_alan_turing@uece.br', '0101000101', true, 'Alan Turing', '23.06.1912', 'files/images/professor/turing.png', 2),
    ('lacan@uece.br', '00153', true, 'Jacques Lacan', '13.04.1901', 'files/images/professor/lacan.png', 1);
    """,
    """
    INSERT INTO api_student (email, enrollment_number, name, password, picture, "majorId_id")
    VALUES 
    ('alicinha@uece.br', '2424', 'Alicia Paiva', 'bob esponja', 'files/images/student/alicia.png', 2),
    ('luiza.psico@uece.br', '11111', 'Luiza Psico', 'sei la vey', 'files/images/student/luiza_dummy_pic.png', 1);
    """,
    """
    INSERT INTO api_event (name, desc_short, desc_detailed, enroll_date_begin, enroll_date_end, picture, workload, minimum_attendances, maximum_enrollments, address, is_online, ended, "ActivityTypeId_id", "professorId_id")
    VALUES 
    ('Breaking Criptograpy', 'How to break encoded messages in a WW', 'How to break encoded messages in a WW, by someone that did it', '2025-01-01', '2025-02-20', 'files/images/event/tm_workshop.png', 10, 1, 200, '', true, false, 1, 1),
    ('Lacanian Theory Seminar', 'I talk about lacanian theory', 'Explanation over the concepts and teory behing lacanian', '2025-01-01', '2025-02-20', 'files/images/event/lacanian_theory.png', 10, 1, 200, '', true, false, 1, 2),
    ('Turing Machine Workshop', 'I talk about TMs', 'Explanation over the concepts and teory behing TMs', '2025-01-01', '2025-02-20', 'files/images/event/tm_workshop.png', 10, 1, 200, '', true, false, 1, 1);

    """,
    """
    INSERT INTO api_eventenrollment ("eventId_id", "studentId_id")
    VALUES (1, 1), (3, 1), (2, 2);
    """,
    """
    INSERT INTO api_eventdate (date, time_begin, time_end, "eventId_id")
    VALUES 
    ('2025-02-21', '8:30', '11:00', 1),
    ('2025-02-21', '8:30', '11:00', 2),
    ('2025-02-21', '13:00', '23:00', 3);
    """,
    """
    INSERT INTO api_attendance (status, "enrollmentId_id", "eventDateId_id")
    VALUES (null, 1, 1), (null, 2, 3), (null, 3, 2);
    """,
    """
    INSERT INTO api_certificate (emission_date, "eventId_id", "studentId_id", file)
    VALUES 
    (NOW(), null, 1, 'files/certificates/cerr.pdf'),
    (NOW(), null, 2, 'cerr.pdf');
    """,
    """
    INSERT INTO api_complementaryactivity (workload, status, description, feedback, "ActivityTypeId_id", "certificateId_id", "studentId_id")
    VALUES 
    (20, null, 'a course of handpainting ive made', '', 2, 1, 1),
    (20, null, 'a course of handpainting ive made', '', 2, 2, 2);
    """
]

# Executa cada comando SQL
for statement in sql_statements:
    cursor.execute(statement)

cursor.close()
connection.commit()
connection.close()

print("Downloading files")


from git import Repo  # pip install gitpython
try:
	Repo.clone_from("git@github.com:SisGeHC-2-0/backend.git", "./files",     branch='dummy_files')
except Exception as e:
	print("Couldn't download the files automatically. \nPlease refer to the branch 'dummy_files' and put both the images and certificates foldes in a new 'files' folder at the root of the project")
