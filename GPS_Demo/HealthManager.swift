import HealthKit

final class HealthManager {
    static let shared = HealthManager()
    private let healthStore = HKHealthStore()

    private var timer: Timer?

    func requestHealthAuth() {
        guard HKHealthStore.isHealthDataAvailable() else { return }

        let steps = HKObjectType.quantityType(forIdentifier: .stepCount)!
        healthStore.requestAuthorization(toShare: [steps], read: []) { _, error in
            if let error = error {
                print("Health auth error:", error)
            }
        }
    }

    /// write 20 stpeps every 10 seconds
    func startWritingFixedSteps() {
        stop()

        timer = Timer.scheduledTimer(withTimeInterval: 10.0, repeats: true) { [weak self] _ in
            self?.writeSteps(20)
        }
        RunLoop.main.add(timer!, forMode: .common)
    }

    func stop() {
        timer?.invalidate()
        timer = nil
    }

    private func writeSteps(_ value: Double) {
        let stepsType = HKQuantityType.quantityType(forIdentifier: .stepCount)!
        let quantity = HKQuantity(unit: .count(), doubleValue: value)

        let end = Date()
        let start = end.addingTimeInterval(-10.0)

        let sample = HKQuantitySample(
            type: stepsType,
            quantity: quantity,
            start: start,
            end: end
        )

        healthStore.save(sample) { success, error in
            print("write:", success, "steps:", value, error ?? "nil")
        }
    }
}
