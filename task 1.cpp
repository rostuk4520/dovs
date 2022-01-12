#include <iostream>
#include <vector>

int main()
{
    setlocale(LC_ALL, "");
    int i;
    std::vector<int> numbers;
    std::cout << "Введите числа: ";
    do {
        std::cin >> i;
        numbers.push_back(i);
    } while (i >= 0);
    for (int a = 0; a < numbers.size(); a++) {
        if (numbers[a] > 2 and numbers[a] < 14) {
            std::cout << numbers[a] << " ";
        }
    }
    std::cout << numbers[numbers.size() - 1] << " ";
}
