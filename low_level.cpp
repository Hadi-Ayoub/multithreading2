#include <chrono>
#include <iostream>
#include <string>
#include <thread>
#include <vector>

#include <Eigen/Dense>
#include <cpr/cpr.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main() {
  std::cout << "--- Minion C++ (Low Level) Démarré ---" << std::endl;

  // URL du Proxy Python
  std::string url = "http://localhost:8000";

  while (true) {
    // request a task
    cpr::Response r = cpr::Get(cpr::Url{url});
    if (r.status_code != 200) {
      std::this_thread::sleep_for(std::chrono::milliseconds(100));
      continue;
    }

    try {
      // parsing the JSON
      auto data = json::parse(r.text);
      int id = data["identifier"];
      int size = data["size"];
      std::cout << "Calcul Tache " << id << " (Taille " << size << ")... "
                << std::flush;

      // convert JSON to Eigen
      std::vector<std::vector<double>> raw_a = data["a"];
      std::vector<double> raw_b = data["b"];

      // fill matrix A
      Eigen::MatrixXd A(size, size);
      for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
          A(i, j) = raw_a[i][j];
        }
      }

      // fill vector B
      Eigen::VectorXd B(size);
      for (int i = 0; i < size; ++i) {
        B(i) = raw_b[i];
      }

      // compute Ax = B
      auto start = std::chrono::high_resolution_clock::now();
      Eigen::VectorXd X = A.partialPivLu().solve(B);
      auto end = std::chrono::high_resolution_clock::now();
      std::chrono::duration<double> elapsed = end - start;

      // convert to a vector for the JSON
      std::vector<double> res_x(X.data(), X.data() + X.size());
      data["x"] = res_x;
      data["time"] = elapsed.count();

      // return the results
      cpr::Response p = cpr::Post(
          cpr::Url{url}, cpr::Header{{"Content-Type", "application/json"}},
          cpr::Body{data.dump()});

      std::cout << "Fait en " << elapsed.count() << "s." << std::endl;

    } catch (const std::exception &e) {
      std::cerr << "Erreur lors du traitement : " << e.what() << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));
    }
  }

  return 0;
}
