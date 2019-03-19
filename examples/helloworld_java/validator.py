from moodleteacher.compiler import JAVAC


def validate(job):
    job.prepare_student_files(remove_directories=False)

    if not job.ensure_files(['HelloWorld.java']):
        job.send_fail_result("Ihre Abgabe muss den Dateinamen 'HelloWorld.java' haben.", "FEHLER: Falscher Dateiname.")
        return

    job.run_compiler(compiler=JAVAC, inputs=['HelloWorld.java'])

    # Run the compilation result.
    exit_code, output = job.run_program('java HelloWorld')
    if "Hello World" not in output:
        job.send_fail_result("Die Ausgabe ihres Programms ist nicht korrekt: " + output, "FEHLER: Falsche Ausgabe.")
    else:
        job.send_pass_result("Super! Das Programm kompiliert und produziert die richtige Ausgabe.", "KORREKT.")
