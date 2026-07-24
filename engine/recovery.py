from core.position_manager import position_manager


class RecoveryEngine:

    def restore(self, engine):

        positions = position_manager.get_all()

        if len(positions) == 0:

            print("RECOVERY : No Active Position")

            return False

        position = positions[0]

        print("=" * 40)
        print("RECOVERY ENGINE")
        print("=" * 40)

        print(f"Coin : {position['coin']}")
        print(f"Buy  : {position['buy_price']}")

        engine.restore_position(position)

        print("RECOVERY SUCCESS")

        return True


recovery = RecoveryEngine()
