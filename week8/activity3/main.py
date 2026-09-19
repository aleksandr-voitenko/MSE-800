from abc import ABC, abstractmethod

class Button(ABC):
    @abstractmethod
    def use(self):
        pass

class Checkbox(ABC):
    @abstractmethod
    def use(self):
        pass

class MacButton(Button):
    def use(self):
        print("Pressed Mac button")

class MacCheckbox(Checkbox):
    def use(self):
        print("Checked Mac button")

class WindowsButton(Button):
    def use(self):
        print("Pressed Window button")

class WindowsCheckbox(Checkbox):
    def use(self):
        print("Checked Window button")

class GUIFactory(ABC):
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

    @abstractmethod
    def create_button(self) -> Button:
        pass

class WindowsGUIFactory(GUIFactory):
    def create_checkbox(self)  -> Checkbox:
        return WindowsCheckbox()

    def create_button(self)  -> Button:
        return WindowsButton()

class MacGUIFactory(GUIFactory):
    def create_checkbox(self)  -> Checkbox:
        return MacCheckbox()

    def create_button(self) -> Button:
        return MacButton()

def main():
    factory: GUIFactory = WindowsGUIFactory()
    button: Button = factory.create_button()
    button.use()

if __name__ == "__main__":
    main()