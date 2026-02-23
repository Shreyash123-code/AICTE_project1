from django.core.management.base import BaseCommand
from studapp.models import Branch, Subject


ENGINEERING_DATA = {
    'Computer Science & Engineering (CSE)': {
        'icon': '💻',
        'subjects': [
            ('Data Structures & Algorithms', '📊'),
            ('Operating Systems', '🖥️'),
            ('Database Management Systems', '🗄️'),
            ('Computer Networks', '🌐'),
            ('Object Oriented Programming', '🧱'),
            ('Software Engineering', '⚙️'),
            ('Artificial Intelligence', '🤖'),
            ('Machine Learning', '🧠'),
            ('Web Development', '🌍'),
            ('Compiler Design', '🔧'),
            ('Theory of Computation', '📐'),
            ('Cyber Security', '🔒'),
            ('Cloud Computing', '☁️'),
            ('Computer Architecture', '🏗️'),
            ('Discrete Mathematics', '🔢'),
        ]
    },
    'Electronics & Communication (ECE)': {
        'icon': '📡',
        'subjects': [
            ('Analog Electronics', '📻'),
            ('Digital Electronics', '💡'),
            ('Signals & Systems', '📈'),
            ('Electromagnetic Theory', '🧲'),
            ('Communication Systems', '📡'),
            ('VLSI Design', '🔌'),
            ('Microprocessors & Microcontrollers', '🧮'),
            ('Control Systems', '🎛️'),
            ('Antenna & Wave Propagation', '📶'),
            ('Digital Signal Processing', '📊'),
            ('Embedded Systems', '🤖'),
            ('Electronic Circuit Design', '⚡'),
        ]
    },
    'Mechanical Engineering (ME)': {
        'icon': '🔩',
        'subjects': [
            ('Engineering Mechanics', '⚖️'),
            ('Thermodynamics', '🌡️'),
            ('Fluid Mechanics', '💧'),
            ('Manufacturing Processes', '🏭'),
            ('Strength of Materials', '💪'),
            ('Machine Design', '⚙️'),
            ('Heat Transfer', '🔥'),
            ('Internal Combustion Engines', '🚗'),
            ('Automobile Engineering', '🚙'),
            ('Robotics', '🤖'),
            ('CAD/CAM', '📐'),
            ('Industrial Engineering', '🏗️'),
        ]
    },
    'Electrical Engineering (EE)': {
        'icon': '⚡',
        'subjects': [
            ('Circuit Theory', '🔌'),
            ('Electrical Machines', '🏭'),
            ('Power Systems', '💡'),
            ('Power Electronics', '⚡'),
            ('Control Systems', '🎛️'),
            ('Electrical Measurements', '📏'),
            ('Switchgear & Protection', '🛡️'),
            ('Renewable Energy Systems', '🌞'),
            ('High Voltage Engineering', '🔋'),
            ('Electrical Drives', '🔄'),
        ]
    },
    'Civil Engineering (CE)': {
        'icon': '🏗️',
        'subjects': [
            ('Structural Analysis', '🏛️'),
            ('Surveying', '🗺️'),
            ('Geotechnical Engineering', '⛰️'),
            ('Concrete Technology', '🧱'),
            ('Transportation Engineering', '🛣️'),
            ('Environmental Engineering', '🌿'),
            ('Hydraulics & Water Resources', '💧'),
            ('Construction Management', '👷'),
            ('Steel Structures', '🏗️'),
            ('Earthquake Engineering', '🌍'),
        ]
    },
    'Information Technology (IT)': {
        'icon': '🖥️',
        'subjects': [
            ('Data Structures & Algorithms', '📊'),
            ('Database Management Systems', '🗄️'),
            ('Computer Networks', '🌐'),
            ('Web Technologies', '🌍'),
            ('Software Engineering', '⚙️'),
            ('Information Security', '🔐'),
            ('Data Mining & Warehousing', '⛏️'),
            ('Mobile Application Development', '📱'),
            ('Big Data Analytics', '📊'),
            ('Internet of Things (IoT)', '🌐'),
        ]
    },
    'Artificial Intelligence & Data Science (AI&DS)': {
        'icon': '🤖',
        'subjects': [
            ('Artificial Intelligence', '🤖'),
            ('Machine Learning', '🧠'),
            ('Deep Learning', '🔬'),
            ('Natural Language Processing', '💬'),
            ('Computer Vision', '👁️'),
            ('Data Science', '📊'),
            ('Big Data Analytics', '📈'),
            ('Statistics & Probability', '🎲'),
            ('Python Programming', '🐍'),
            ('Neural Networks', '🧬'),
        ]
    },
    'Common / First Year': {
        'icon': '📚',
        'subjects': [
            ('Engineering Mathematics I', '📐'),
            ('Engineering Mathematics II', '📐'),
            ('Engineering Mathematics III', '📐'),
            ('Engineering Physics', '🔬'),
            ('Engineering Chemistry', '🧪'),
            ('Basic Electrical Engineering', '⚡'),
            ('Basic Electronics', '💡'),
            ('Engineering Graphics', '📏'),
            ('Programming in C', '💻'),
            ('Communication Skills', '🗣️'),
            ('Environmental Studies', '🌿'),
            ('Engineering Mechanics', '⚖️'),
        ]
    },
}


class Command(BaseCommand):
    help = 'Populate the database with engineering branches and subjects'

    def handle(self, *args, **options):
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

        self.stdout.write(self.style.SUCCESS('\n✅ All engineering branches and subjects populated!'))
