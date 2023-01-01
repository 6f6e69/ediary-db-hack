import os
import argparse
import pathlib
import django
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from datacenter.models import (Schoolkid, Mark, Chastisement, Lesson,
                               Subject, Commendation)


def validate_schoolkid(schoolkid: str) -> Schoolkid:
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid)
    except Schoolkid.MultipleObjectsReturned:
        raise argparse.ArgumentTypeError('Find multiple schoolkids, '
                                         'refine your request.')
    except Schoolkid.DoesNotExist:
        raise argparse.ArgumentTypeError('Schoolkid not found.')


def validate_subject(subject_title: str) -> str:
    if not Subject.objects.filter(title=subject_title).exists():
        raise argparse.ArgumentTypeError(f'Subject {subject_title} '
                                         'does not exists.')
    return subject_title


def fix_marks(schoolkid: Schoolkid) -> None:
    bad_marks = Mark.objects.filter(
                schoolkid__full_name__contains=schoolkid.full_name,
                points__lte=3)
    if not bad_marks:
        print('Bad marks not found, nothing to fix.')
        return
    print(f'Found {bad_marks.count()} bad marks.')
    bad_marks.update(points=5)
    print('Bad mark succesfully replaced.')


def remove_chastisements(schoolkid: Schoolkid) -> None:
    chastisements = Chastisement.objects.filter(
                    schoolkid__full_name__contains=schoolkid.full_name)
    if not chastisements:
        print('Chastisements not found.')
        return
    print(f'Found {chastisements.count()} chastisements.')
    chastisements.delete()
    print('Chastisements successfully removed.')


def read_commendations_from_file(filepath: pathlib.Path) -> list:
    if not filepath.exists() and filepath.is_file:
        print(f"Can't find file {filepath}.")
        exit(1)
    try:
        with open(filepath, 'r') as file:
            commendations = file.read().splitlines()
    except OSError:
        print(f"Can't open {filepath}")
    return commendations


def create_commendation(schoolkid: Schoolkid, subject_title: str) -> None:
    try:
        last_subject_lesson = Lesson.objects.filter(
                                     subject__title=subject_title,
                                     year_of_study=schoolkid.year_of_study,
                                     group_letter=schoolkid.group_letter
                                                    ).order_by('-date').first()
    except Lesson.DoesNotExist:
        raise LookupError(f'No lessons for subject {subject_title}')
    text = random.choice(read_commendations_from_file(args.file_path))
    new_commendation = Commendation(text=text,
                                    created=last_subject_lesson.date,
                                    schoolkid=schoolkid,
                                    subject=last_subject_lesson.subject,
                                    teacher=last_subject_lesson.teacher)
    new_commendation.save()
    print(f'Created commendation with text "{new_commendation.text}".')


if __name__ == '__main__':
    parser_description = ('Script helps you easily convert bad marks to '
                          'good, delete chastisements or add new'
                          'commendations.')
    parser = argparse.ArgumentParser(description=parser_description)
    parser.add_argument('--schoolkid',
                        help='name of scholkid',
                        type=validate_schoolkid,
                        required=True)
    parser.add_argument('--fix-bad-marks',
                        dest='fix_bad_marks',
                        help='fix bad marks',
                        action='store_true')
    parser.add_argument('--rm-chastisements',
                        dest='rm_chastisements',
                        help='remove chastisements',
                        action='store_true')
    subparsers = parser.add_subparsers(dest='command')
    parser_commendations = subparsers.add_parser('add_commendation')
    parser_commendations.add_argument('--subject',
                                      help='subject to add commendation',
                                      type=validate_subject,
                                      required=True)
    parser_commendations.add_argument('--file-path',
                                      dest='file_path',
                                      help='path to file with commendations',
                                      type=pathlib.Path,
                                      default='commendations.txt')
    args = parser.parse_args()
    if args.fix_bad_marks:
        fix_marks(args.schoolkid)
    if args.rm_chastisements:
        remove_chastisements(args.schoolkid)
    if args.command == 'add_commendation':
        create_commendation(args.schoolkid, args.subject)
