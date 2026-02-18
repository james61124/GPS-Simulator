import Foundation
import HealthKit

class HealthManager {
    static let shared = HealthManager()
    let healthStore = HKHealthStore()
    
    // Request permission to write health data
    func requestHealthAuthorization() {
        // Check if HealthKit is available on this device
        guard HKHealthStore.isHealthDataAvailable() else {
            print("HealthKit is not available on this device.")
            return
        }
        
        // Define the data types we want to write (Steps)
        let typesToShare: Set = [
            HKQuantityType.quantityType(forIdentifier: .stepCount)!
        ]
        
        // Request authorization from the user
        healthStore.requestAuthorization(toShare: typesToShare, read: nil) { success, error in
            if success {
                print("HealthKit authorization granted.")
            } else {
                print("HealthKit authorization failed: \(String(describing: error?.localizedDescription))")
            }
        }
    }
    
    // Add a specific amount of steps to the Health database immediately
    func addBulkSteps(count: Double, completion: @escaping (Bool) -> Void) {
        guard let stepType = HKQuantityType.quantityType(forIdentifier: .stepCount) else {
            completion(false)
            return
        }
        let now = Date()
        let startDate = now.addingTimeInterval(-60)
        let quantity = HKQuantity(unit: HKUnit.count(), doubleValue: count)
        let sample = HKQuantitySample(type: stepType, quantity: quantity, start: startDate, end: now)
        
        healthStore.save(sample) { success, error in
            DispatchQueue.main.async {
                if success {
                    print("Successfully added \(Int(count)) steps.")
                } else {
                    print("Error: \(String(describing: error?.localizedDescription))")
                }
                // Notify the UI whether it was successful or not
                completion(success)
            }
        }
    }
}