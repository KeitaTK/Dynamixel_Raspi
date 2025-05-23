"""
Windows環境用Dynamixel制御クラス
ポートの占有特性がUbuntuと異なり1モーター1クラスができないため、id周りが少し異なる。
"""

import sys
from dynamixel_sdk import *  # Uses Dynamixel SDK library

class Dynamixel:
    def __init__(self, port, baudrate):
        # getch for Linux
        def getch():
            return sys.stdin.read(1)

        # DYNAMIXEL Model definition
        self.__MY_DXL = "X_SERIES"
        self.__ADDR_TORQUE_ENABLE = 64
        self.__ADDR_OPERATION_MODE = 11

        self.__ADDR_VELOCITY_LIMIT = 44
        self.__ADDR_GOAL_VELOCITY = 104
        self.__ADDR_PRESENT_VELOCITY = 128

        self.__ADDR_MAXIMUM_POSITION = 48
        self.__ADDR_MINIMUM_POSITION = 52
        self.__ADDR_GOAL_POSITION    = 116
        self.__ADDR_PRESENT_POSITION = 132

        self.__BAUDRATE = baudrate
        self.__PROTOCOL_VERSION = 2.0

        # Raspberry Piでは/dev/ttyUSB0や/dev/ttyS0などを指定
        self.__DEVICENAME = port

        self.__TORQUE_ENABLE = 1
        self.__TORQUE_DISABLE = 0

        self.__VELOCITY_MODE = 1
        self.__POSITION_MODE = 3
        self.__EX_POSITION_MODE = 4

        # PortHandlerとPacketHandlerの初期化
        self.__portHandler = PortHandler(self.__DEVICENAME)
        self.__packetHandler = PacketHandler(self.__PROTOCOL_VERSION)

        # ポートを開く
        if self.__portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            quit()

        # ボーレート設定
        if self.__portHandler.setBaudRate(self.__BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            quit()

        # Set port baudrate
        if self.__portHandler.setBaudRate(self.__BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            quit()

        

    def set_mode_velocity(self,id):
        """速度制御モードに設定

        Parameter
        ----------
        id : int
            IDを指定
        """
        dxl_comm_result, dxl_error = self.__packetHandler.write1ByteTxRx(
            self.__portHandler,
            id,
            self.__ADDR_OPERATION_MODE,
            self.__VELOCITY_MODE,
        )
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.__packetHandler.getRxPacketError(dxl_error))
        
        # Initialize Goal Velocity
        self.write_velocity(0,0)


    def set_mode_position(self,id):
        """角度制御モードに設定

        Parameter
        ----------
        id : int
            IDを指定
        """
        dxl_comm_result, dxl_error = self.__packetHandler.write1ByteTxRx(
            self.__portHandler,
            id,
            self.__ADDR_OPERATION_MODE,
            self.__POSITION_MODE,
        )
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.__packetHandler.getRxPacketError(dxl_error))

    def set_mode_ex_position(self,id):
        """拡張角度制御モードに設定

        Parameter
        ----------
        id : int
            IDを指定
        """
        dxl_comm_result, dxl_error = self.__packetHandler.write1ByteTxRx(
            self.__portHandler,
            id,
            self.__ADDR_OPERATION_MODE,
            self.__EX_POSITION_MODE,
        )
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.__packetHandler.getRxPacketError(dxl_error))

    def set_max_velocity(self,id,max_velocity):
        """速度制御時最大回転速度を設定

        Parameters
        ------------
        id : int
            IDを指定
        max_velocity : int
            最大回転速度 (通常265)
        
        """
        dxl_comm_result, dxl_error = self.__packetHandler.write4ByteTxRx(
            self.__portHandler,
            id,
            self.__ADDR_VELOCITY_LIMIT,
            max_velocity,
        )
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.__packetHandler.getRxPacketError(dxl_error))
        print("SET MAX VELOCITY")

    def set_min_max_position(self,id,min_position,max_position):
        """角度制御時最小最大位置を設定

        Parameter
        ----------
        id : int
            IDを指定
        min_position : 
            最小位置 (通常 0)
        max_position : 
            最大位置 (通常 4095)
        """
        # Write Min Position Limit
        dxl_comm_result, dxl_error = self.__packetHandler.write4ByteTxRx(self.__portHandler, id, self.__ADDR_MINIMUM_POSITION, min_position)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.__packetHandler.getRxPacketError(dxl_error))
        print("SET MIN POSITION")

        # Write Max Position Limit
        dxl_comm_result, dxl_error = self.__packetHandler.write4ByteTxRx(self.__portHandler, id, self.__ADDR_MAXIMUM_POSITION, max_position)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.__packetHandler.getRxPacketError(dxl_error))
        print("SET MAX POSITION")
        
    


    def enable_torque(self,id):
        """トルクをオンにする

        Parameter
        ----------
        id : int
            IDを指定
        """
        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = self.__packetHandler.write1ByteTxRx(
            self.__portHandler,
            id,
            self.__ADDR_TORQUE_ENABLE,
            self.__TORQUE_ENABLE,
        )
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.__packetHandler.getRxPacketError(dxl_error))

    def disable_torque(self,id):
        """トルクをオフにする

        Parameter
        ----------
        id : int
            IDを指定
        """
        dxl_comm_result, dxl_error = self.__packetHandler.write1ByteTxRx(
            self.__portHandler,
            id,
            self.__ADDR_TORQUE_ENABLE,
            self.__TORQUE_DISABLE,
        )
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.__packetHandler.getRxPacketError(dxl_error))

    def write_velocity(self,id, vel):
        """目標回転速度を送信する

        Parameter
        ----------
        id : int
            IDを指定
        vel : int
            最大速度以下の速度を指定する (ex. -128 ~ 128 )
        """
        dxl_comm_result, dxl_error = self.__packetHandler.write4ByteTxRx(
            self.__portHandler,
            id,
            self.__ADDR_GOAL_VELOCITY,
            vel,
        )
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.__packetHandler.getRxPacketError(dxl_error))
        print("SET POSITION")
        print("[ID:%03d]  GoalVel:%03d" % (id, vel))

    def read_velocity(self,id):
        """現在回転速度を受信する

        Parameter
        ----------
        id : int
            IDを指定

        Returns
        -------
        dxl_present_velocity : int
            現在の回転速度 (ex. -128 ~ 128 )
        """
        (
            dxl_present_velocity,
            dxl_comm_result,
            dxl_error,
        ) = self.__packetHandler.read4ByteTxRx(
            self.__portHandler, id, self.__ADDR_PRESENT_VELOCITY
        )
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.__packetHandler.getRxPacketError(dxl_error))

        print(
            "[ID:%03d]  PresVel:%03d"
            % (id, dxl_present_velocity)
        )

        return dxl_present_velocity
    
    def write_position(self,id,pos):
        """現在位置を受信する

        Parameter
        ----------
        id : int
            IDを指定
        pos : int
            目標位置 ( ex. 0 ~ 4095 )
            0(MinPositionLimit)~1(MaxPositionLimit)で示される位置の値
        """
        dxl_comm_result, dxl_error = self.__packetHandler.write4ByteTxRx(self.__portHandler, id, self.__ADDR_GOAL_POSITION, pos)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.__packetHandler.getRxPacketError(dxl_error))
        print("SET POSITION")
        print("[ID:%03d]  GoalPos:%03d" % (id, pos))
    
    
    def read_position(self,id): 
        """現在の位置の読みとり

        Parameter
        ----------
        id : int
            IDを指定

        Returns
        -------
        dxl_present_position : int
            0~4095までの値
        """
        dxl_present_position, dxl_comm_result, dxl_error = self.__packetHandler.read4ByteTxRx(self.__portHandler, id, self.__ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.__packetHandler.getRxPacketError(dxl_error))
            
        print("[ID:%03d]  PresPos:%03d" % (id, dxl_present_position))
        
        return dxl_present_position

    def close_port(self):
        self.__portHandler.closePort()