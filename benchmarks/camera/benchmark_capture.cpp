// Benchmark of OpenCV++ camera capture performance.
//
// Summary:
// 1) Average capture rate is around 20ms.
// 2) Performance overhead is almost neglegible comparing to python wrappers:
//    20ms vs 30ms.

#include <ctime>
#include <iostream>
#include <vector>

#include "opencv2/opencv.hpp"
using namespace cv;


class timer {
public:
  timer() : t_(clock()) {}
  void start() { t_ = clock(); }
  float elapsed() { return float(clock() - t_) / CLOCKS_PER_SEC; }
private:
  clock_t t_;
};

int main() {
  timer t;
  VideoCapture cap(0);
  if (!cap.isOpened()) {
    return -1;
  }

  std::vector<float> timings;
  for (int i = 0; i < 10; ++i) {
    Mat frame;
    t.start();
    cap >> frame;
    timings.push_back(t.elapsed()); 
  }
  std::cout << "Camera capture timings with CV++:" << std::endl;
  for (const auto item : timings) {
    std::cout << item << ";" << std::endl;
  }
  return 0;
}
