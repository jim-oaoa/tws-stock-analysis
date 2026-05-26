import unittest
from src.valuation.models import FinancialQuarterly, FundamentalZone, TechnicalState, HybridSignal
from src.valuation.engine import compute_net_value, compute_zones, determine_signal

class TestValuationEngine(unittest.TestCase):

    def test_compute_net_value(self):
        """Test Case 1: Verify accumulated NetValue from FinancialQuarterly records."""
        records = [
            FinancialQuarterly(symbol="AAPL", year=2023, quarter=1, eps=1.0, oci=0.1, other_items=0.05, dividends=0.2, adjustment_amount=0.0),
            FinancialQuarterly(symbol="AAPL", year=2023, quarter=2, eps=1.2, oci=0.2, other_items=0.1, dividends=0.2, adjustment_amount=0.1),
            FinancialQuarterly(symbol="AAPL", year=2023, quarter=3, eps=0.8, oci=-0.1, other_items=0.0, dividends=0.2, adjustment_amount=-0.05),
        ]
        
        # Q1 sum: 1.0 + 0.1 + 0.05 + 0.2 + 0.0 = 1.35
        # Q2 sum: 1.2 + 0.2 + 0.1 + 0.2 + 0.1 = 1.8
        # Q3 sum: 0.8 - 0.1 + 0.0 + 0.2 - 0.05 = 0.85
        # Accumulated: 1.35 -> 3.15 -> 4.0
        
        grid = compute_net_value(records, initial_net_value=0.0)
        
        self.assertEqual(grid[0].accumulated_net_value, 1.35)
        self.assertAlmostEqual(grid[1].accumulated_net_value, 3.15, places=10)
        self.assertEqual(grid[2].accumulated_net_value, 4.0)

    def test_compute_zones(self):
        """Test Case 2: Verify baseline NetValue mapping to Fish-Bone zones."""
        net_value = 100.0
        zones = compute_zones(net_value)
        
        # Multipliers: Head (0.85x), Body (1.00x), Tail Low (1.15x), Tail High (1.30x), Bone (2.00x)
        self.assertEqual(zones.fish_head, 85.0)
        self.assertEqual(zones.fish_body, 100.0)
        self.assertEqual(zones.fish_tail_low, 115.0)
        self.assertEqual(zones.fish_tail_high, 130.0)
        self.assertEqual(zones.fish_bone, 200.0)

    def test_hybrid_signal_matrix(self):
        """Test Case 3: Verify the Hybrid Signal Matrix logic."""
        # The prompt mentions TechnicalState.FISH_HEAD and TechnicalState.FISH_TAIL, 
        # but based on the code, these are ValuationZones. 
        # The signals are based on FundamentalZone and TechnicalState.
        
        # FundamentalZone.UNDERVALUED + TechnicalState.BULLISH -> STRONG_BUY
        signal, _ = determine_signal(FundamentalZone.UNDERVALUED, TechnicalState.BULLISH)
        self.assertEqual(signal, HybridSignal.STRONG_BUY)
        
        # FundamentalZone.OVERVALUED + TechnicalState.BEARISH -> STRONG_SELL
        signal, _ = determine_signal(FundamentalZone.OVERVALUED, TechnicalState.BEARISH)
        self.assertEqual(signal, HybridSignal.STRONG_SELL)
        
        # FundamentalZone.OVERVALUED + TechnicalState.OVEREXTENDED -> STRONG_SELL
        signal, _ = determine_signal(FundamentalZone.OVERVALUED, TechnicalState.OVEREXTENDED)
        self.assertEqual(signal, HybridSignal.STRONG_SELL)

if __name__ == "__main__":
    unittest.main()
