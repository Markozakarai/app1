from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, CourseSection, Lesson, Testimonial

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed demo data for Marco Academy platform'

    def handle(self, *args, **options):
        if not User.objects.filter(email='admin@marcoacademy.com').exists():
            User.objects.create_superuser(
                email='admin@marcoacademy.com',
                full_name='ماركو زكريا',
                phone='01000000000',
                password='admin123456',
            )
            self.stdout.write(self.style.SUCCESS('Admin created: admin@marcoacademy.com / admin123456'))

        if not User.objects.filter(email='student@example.com').exists():
            User.objects.create_user(
                email='student@example.com',
                full_name='أحمد محمد',
                phone='01100000000',
                password='student123',
            )
            self.stdout.write(self.style.SUCCESS('Student created: student@example.com / student123'))

        if not Course.objects.exists():
            course1 = Course.objects.create(
                title='تعلم Django من الصفر',
                slug='django-from-scratch',
                short_description='كورس شامل لتعلم Django وبناء تطبيقات ويب احترافية',
                full_description='في هذا الكورس ستتعلم Django من الأساسيات حتى بناء منصة تعليمية كاملة. يشمل المشروع العملي بناء REST APIs، Authentication، Templates، وMedia Uploads.',
                price=1500,
                duration='8 أسابيع',
                skills='Python, Django, HTML, CSS, Bootstrap, SQLite, PostgreSQL',
                projects='مدونة, متجر إلكتروني, منصة تعليمية',
                is_published=True,
                is_featured=True,
            )
            section1 = CourseSection.objects.create(course=course1, title='الأسبوع الأول - المقدمة', order=1)
            Lesson.objects.create(section=section1, title='مقدمة عن Django', lesson_type='video', description='تعرف على Django ولماذا نستخدمه', order=1)
            Lesson.objects.create(section=section1, title='إعداد البيئة', lesson_type='video', description='تثبيت Python و Django', order=2)
            section2 = CourseSection.objects.create(course=course1, title='الأسبوع الثاني - Models & Admin', order=2)
            Lesson.objects.create(section=section2, title='إنشاء Models', lesson_type='video', order=1)
            Lesson.objects.create(section=section2, title='ملخص PDF', lesson_type='pdf', order=2)
            course1.update_lesson_count()

            Course.objects.create(
                title='JavaScript للمبتدئين',
                slug='javascript-basics',
                short_description='تعلم أساسيات JavaScript وبناء تفاعلات الويب',
                full_description='كورس عملي يغطي المتغيرات، الدوال، DOM، Events، و Fetch API.',
                price=800,
                duration='4 أسابيع',
                skills='JavaScript, DOM, ES6, Async/Await',
                projects='Todo App, Weather App',
                is_published=True,
            )
            self.stdout.write(self.style.SUCCESS('Demo courses created'))

        if not Testimonial.objects.exists():
            Testimonial.objects.create(
                student_name='محمد علي',
                student_title='مطور ويب',
                content='كورس Django غيّر مساري المهني. الشرح واضح والمشاريع العملية ممتازة.',
                rating=5,
            )
            Testimonial.objects.create(
                student_name='سارة أحمد',
                student_title='طالبة علوم حاسب',
                content='أفضل منصة تعليمية بالعربي. الدعم سريع والمحتوى منظم بشكل رائع.',
                rating=5,
            )
            Testimonial.objects.create(
                student_name='خالد يوسف',
                student_title='Freelancer',
                content='بفضل ماركو Academy حصلت على أول مشروع freelance لي في تطوير الويب.',
                rating=4,
            )
            self.stdout.write(self.style.SUCCESS('Testimonials created'))

        self.stdout.write(self.style.SUCCESS('Seed completed!'))
