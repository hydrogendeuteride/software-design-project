import threading
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI


# execute_command를 제어하는 콜백 함수
# -> 이 함수에서 시그널을 입력받고 처리하는 로직을 구성하면, 알아서 GUI에 연동이 됩니다.

def execute_command_callback(command, car_controller):
    # 임찬우
    if command == "ENGINE_BTN":
        car_controller.toggle_engine()  # 시동 ON / OFF

    # 송혜주
    elif command == "ACCELERATE":
        car_controller.accelerate()  # 속도 +10
        if (car_controller.get_speed() >= 20):  # 속도가 20일 때 차 문을 잠그도록 함.
            car_controller.car.lock_left_door()
            car_controller.car.lock_right_door()
    elif command == "BRAKE":
        car_controller.brake()  # 속도 -10


    # 주정윤
    elif command == "LOCK":
        car_controller.lock_vehicle()  # 차량잠금
    elif command == "UNLOCK":
        car_controller.unlock_vehicle()  # 차량잠금해제


    # 이재헌
    elif command == "LEFT_DOOR_LOCK":
        # 차량이 잠겨있지 않고, 왼쪽문이 닫혀있을 때만 왼쪽문 잠금
        if not car_controller.get_lock_status() == "LOCKED":
            if car_controller.get_left_door_status() == "CLOSED":
                car_controller.car.lock_left_door()  # 왼쪽문 잠금

    elif command == "LEFT_DOOR_UNLOCK":
        # 차량이 잠겨있지 않고, 왼쪽문이 닫혀있고, 속도가 0일 때만 왼쪽문 잠금해제
        if not car_controller.get_lock_status() == "LOCKED":
            if car_controller.get_left_door_status() == "CLOSED":
                if (car_controller.get_speed() == 0):
                    car_controller.unlock_left_door()  # 왼쪽문 잠금해제

    elif command == "RIGHT_DOOR_LOCK":
        # 차량이 잠겨있지 않고, 오른쪽문이 닫혀있을 때만 오른쪽문 잠금
        if not car_controller.get_lock_status() == "LOCKED":
            if car_controller.get_right_door_status() == "CLOSED":
                car_controller.lock_right_door()

    elif command == "RIGHT_DOOR_UNLOCK":
        # 차량이 잠겨있지 않고, 오른쪽문이 닫혀있고, 속도가 0일 때만 오른쪽문 잠금해제
        if not car_controller.get_lock_status() == "LOCKED":
            if car_controller.get_right_door_status() == "CLOSED":
                if (car_controller.get_speed() == 0):
                    car_controller.unlock_right_door()  # 왼쪽문 잠금해제



    # 한재일
    elif command == "LEFT_DOOR_OPEN":
        car_controller.open_left_door()  # 왼쪽문 열기
    elif command == "LEFT_DOOR_CLOSE":
        car_controller.close_left_door()  # 왼쪽문 닫기
    elif command == "RIGHT_DOOR_OPEN":
        car_controller.open_right_door()  # 오른쪽문 열기
    elif command == "RIGHT_DOOR_CLOSE":
        car_controller.close_right_door()  # 오른쪽문 닫기


    # 송국선
    elif command == "TRUNK_OPEN":
        # car_controller.open_trunk()  # 트렁크 열기
        trunk_open_condition_check(car_controller)
    elif command == "TRUNK_CLOSE":
        # car_controller.close_trunk()  # 트렁크 닫기
        trunk_close_condition_check(car_controller)


def can_operate_trunk(car_controller, trunk_status):
    return (
        car_controller.get_speed() == 0 and
        not car_controller.get_lock_status() and
        car_controller.get_trunk_status() == trunk_status
    )


def trunk_open_condition_check(car_controller):
    if can_operate_trunk(car_controller, trunk_status=True):
        car_controller.car.open_trunk()


def trunk_close_condition_check(car_controller):
    if can_operate_trunk(car_controller, trunk_status=False):
        car_controller.car.close_trunk()


# 파일 경로를 입력받는 함수
# -> 가급적 수정하지 마세요.
#    테스트의 완전 자동화 등을 위한 추가 개선시에만 일부 수정이용하시면 됩니다. (성적 반영 X)
def file_input_thread(gui):
    while True:
        file_path = input(
            "Please enter the command file path (or 'exit' to quit): ")

        if file_path.lower() == 'exit':
            print("Exiting program.")
            break

        # 파일 경로를 받은 후 GUI의 mainloop에서 실행할 수 있도록 큐에 넣음
        gui.window.after(0, lambda: gui.process_commands(file_path))


# 메인 실행
# -> 가급적 main login은 수정하지 마세요.
if __name__ == "__main__":
    car = Car()
    car_controller = CarController(car)

    # GUI는 메인 스레드에서 실행
    gui = CarSimulatorGUI(car_controller,
                          lambda command: execute_command_callback(command,
                                                                   car_controller))

    # 파일 입력 스레드는 별도로 실행하여, GUI와 병행 처리
    input_thread = threading.Thread(target=file_input_thread, args=(gui,))
    input_thread.daemon = True  # 메인 스레드가 종료되면 서브 스레드도 종료되도록 설정
    input_thread.start()

    # GUI 시작 (메인 스레드에서 실행)
    gui.start()
