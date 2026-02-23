from django.core.management.base import BaseCommand
from studapp.models import Branch, Subject


ENGINEERING_DATA = {
    'First Year (FE)': {
        'icon': '📚',
        'subjects': [
            ('Engineering Mathematics-I', '📐'),
            ('Engineering Mechanics', '⚖️'),
            ('Engineering Graphics', '📏'),
            ('Basic Electronics Engineering', '💡'),
            ('Basic Electrical Engineering', '⚡'),
            ('Engineering Physics', '🔬'),
            ('Engineering Chemistry', '🧪'),
            ('Fundamentals of Programming Language', '💻'),
        ]
    },
    'Computer Engineering': {
        'icon': '💻',
        'subjects': [
            # SE Sem 3
            ('Data Structures', '📊'),
            ('Object Oriented Programming', '🧱'),
            ('Computer Graphics', '🎨'),
            ('Operating Systems', '🖥️'),
            ('Digital Electronics and Logical Design', '💡'),
            # SE Sem 4
            ('Database Management Systems', '🗄️'),
            ('Discrete Mathematics', '🔢'),
            ('Computer Organization and Microprocessor', '🧮'),
            ('Internet of Things', '🌐'),
            ('Web Development', '🌍'),
            # TE Sem 5
            ('Theory of Computation', '📐'),
            ('Systems Programming & Operating System', '⚙️'),
            ('Computer Networks & Security', '🔒'),
            # TE Sem 6
            ('Data Science & Big Data Analytics', '📈'),
            ('Web Technology', '🌐'),
            ('Artificial Intelligence', '🤖'),
            ('Cloud Computing', '☁️'),
            # BE Sem 7
            ('Design and Analysis of Algorithms', '📊'),
            ('Machine Learning', '🧠'),
            ('Blockchain Technology', '🔗'),
        ]
    },
    'Mechanical Engineering': {
        'icon': '🔩',
        'subjects': [
            # SE Sem 3
            ('Solid Mechanics', '💪'),
            ('Engineering Materials & Metallurgy', '🔧'),
            ('Engineering Mathematics-III', '📐'),
            ('Fluid Mechanics', '💧'),
            # SE Sem 4
            ('Manufacturing Processes-I', '🏭'),
            # TE Sem 5
            ('Numerical & Statistical Methods', '🔢'),
            ('Heat & Mass Transfer', '🔥'),
            ('Design of Machine Elements', '⚙️'),
            ('Mechatronics', '🤖'),
            # TE Sem 6
            ('Artificial Intelligence & Machine Learning', '🧠'),
            ('Computer Aided Engineering', '🖥️'),
            ('Design of Transmission Systems', '⚙️'),
            # BE Sem 7
            ('Computer Aided Design / Computer Aided Engineering', '📐'),
            ('Mechatronics / Industrial Automation', '🏭'),
            ('Design of Transmission Systems II', '⚙️'),
            # BE Sem 8
            ('Computer Integrated Manufacturing', '🏗️'),
            ('Robotics and Flexible Manufacturing Systems', '🤖'),
        ]
    },
    'Information Technology': {
        'icon': '🖥️',
        'subjects': [
            # SE Sem 3
            ('Data Structures & Algorithms', '📊'),
            ('Object-Oriented Programming', '🧱'),
            ('Basic Computer Networks', '🌐'),
            ('Digital Electronics and Logical Design', '💡'),
            # SE Sem 4
            ('Database Management Systems (DBMS)', '🗄️'),
            ('Computer Graphics', '🎨'),
            ('Probability & Statistics', '🎲'),
            ('Processor Architecture', '🧮'),
            # TE Sem 5
            ('Theory of Computation', '📐'),
            ('Operating Systems', '🖥️'),
            ('Machine Learning', '🧠'),
            ('Human Computer Interaction', '🖱️'),
            # TE Sem 6
            ('Computer Networks & Security', '🔒'),
            ('Data Science and Big Data Analytics', '📈'),
            ('Web Application Development', '🌍'),
            ('Cloud Computing', '☁️'),
            # BE Sem 7
            ('Information and Cyber Security', '🔐'),
            ('Mobile Computing', '📱'),
            ('Artificial Intelligence', '🤖'),
            # BE Sem 8
            ('Deep Learning', '🔬'),
            ('High Performance Computing', '⚡'),
        ]
    },
    'Civil Engineering': {
        'icon': '🏗️',
        'subjects': [
            # SE Sem 3
            ('Mechanics of Structures', '🏛️'),
            ('Surveying', '🗺️'),
            ('Building Construction & Materials', '🧱'),
            ('Engineering Mathematics-III', '📐'),
            # SE Sem 4
            ('Concrete Technology', '🧱'),
            ('Structural Analysis', '🏛️'),
            ('Fluid Mechanics', '💧'),
            ('Engineering Mathematics-IV', '📐'),
            # TE Sem 5
            ('Hydrology and Water Resources', '💧'),
            ('Water Supply Engineering', '🚰'),
            ('Design of Steel Structures', '🏗️'),
            ('Engineering Economics and Financial Management', '💰'),
            # TE Sem 6
            ('Waste Water Engineering', '🚿'),
            ('Design of Reinforced Concrete Structures', '🏛️'),
            ('Remote Sensing and GIS', '🛰️'),
            ('Architecture and Town Planning', '🏘️'),
            ('Solid Waste Management', '♻️'),
            # BE Sem 7
            ('Foundation Engineering', '⛰️'),
            ('Transportation Engineering', '🛣️'),
            ('Integrated Water Resources Planning and Management', '💧'),
            # BE Sem 8
            ('Dams and Hydraulic Structures', '🌊'),
            ('Quantity Surveying, Contracts & Tenders', '📋'),
        ]
    },
}


class Command(BaseCommand):
    help = 'Populate the database with engineering branches and subjects'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing branches and subjects before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing all existing branches and subjects...'))
            Subject.objects.all().delete()
            Branch.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared!\n'))

        for branch_name, data in ENGINEERING_DATA.items():
            branch, created = Branch.objects.get_or_create(
                name=branch_name,
                defaults={'icon': data['icon']}
            )
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  Branch: {branch_name} [{status}]')

            for subj_name, subj_icon in data['subjects']:
                subj, created = Subject.objects.get_or_create(
                    name=subj_name,
                    branch=branch,
                    defaults={'icon': subj_icon}
                )
                s_status = '✅' if created else '⏭️'
                self.stdout.write(f'    {s_status} {subj_name}')

        self.stdout.write(self.style.SUCCESS('\n✅ All branches and subjects populated!'))
