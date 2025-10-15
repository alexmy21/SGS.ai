# triangulation.py
import numpy as np
from typing import Any, List, Set, Dict, Tuple
from collections import defaultdict
import math

class SemanticTriangulation:
    """
    Implement multiple triangulation methods for HLLSet token disambiguation
    """
    
    def __init__(self, hll_wrapper, num_seeds: int = 8):
        self.hll_wrapper = hll_wrapper
        self.num_seeds = num_seeds
        self.seeds = self._generate_independent_seeds()
        
    def _generate_independent_seeds(self) -> List[int]:
        """Generate independent hash seeds for triangulation"""
        # Use prime numbers to ensure independence
        base_seed = 42
        return [base_seed * (i + 1) * 2654435761 % (2**31) 
                for i in range(self.num_seeds)]
    
    def create_multi_seed_observations(self, tokens: List[str]) -> Dict[int, Any]:
        """Create HLLSet observations using multiple seeds"""
        observations = {}
        
        for seed in self.seeds:
            hll_data = self.hll_wrapper.create_set(tokens, seed=seed)
            observations[seed] = hll_data
            
        return observations
    
    def basic_triangulation(self, observations: Dict[int, Any], 
                          candidate_tokens: List[str]) -> Set[str]:
        """
        Basic triangulation: intersection across all seeds
        """
        # For each seed, determine which candidate tokens are consistent
        seed_consistent_tokens = []
        
        for seed, obs in observations.items():
            # In real implementation, we'd check bit positions
            # For demo, we'll simulate consistency check
            consistent_tokens = self._get_consistent_tokens(obs, candidate_tokens, seed)
            seed_consistent_tokens.append(set(consistent_tokens))
        
        # Return intersection across all seeds
        if seed_consistent_tokens:
            return set.intersection(*seed_consistent_tokens)
        return set()
    
    def weighted_triangulation(self, observations: Dict[int, Any],
                             candidate_tokens: List[str],
                             seed_weights: Dict[int, float] = None) -> Dict[str, float]:
        """
        Weighted triangulation: tokens get scores based on seed consistency
        """
        if seed_weights is None:
            seed_weights = {seed: 1.0 for seed in observations.keys()}
        
        token_scores = defaultdict(float)
        
        for seed, obs in observations.items():
            weight = seed_weights[seed]
            consistent_tokens = self._get_consistent_tokens(obs, candidate_tokens, seed)
            
            for token in consistent_tokens:
                token_scores[token] += weight
        
        # Normalize scores
        max_score = max(token_scores.values()) if token_scores else 1.0
        normalized_scores = {token: score/max_score 
                           for token, score in token_scores.items()}
        
        return normalized_scores
    
    def progressive_triangulation(self, observations: Dict[int, Any],
                                candidate_tokens: List[str],
                                confidence_threshold: float = 0.8) -> Dict[str, Any]:
        """
        Progressive triangulation: add seeds one by one until convergence
        """
        current_candidates = set(candidate_tokens)
        convergence_history = []
        used_seeds = []
        
        for i, (seed, obs) in enumerate(observations.items()):
            used_seeds.append(seed)
            
            # Get consistent tokens for current seed
            consistent_tokens = set(self._get_consistent_tokens(obs, list(current_candidates), seed))
            
            # Update candidate set
            prev_size = len(current_candidates)
            current_candidates = current_candidates.intersection(consistent_tokens)
            new_size = len(current_candidates)
            
            convergence_history.append({
                'iteration': i,
                'seeds_used': len(used_seeds),
                'candidate_size': new_size,
                'reduction': prev_size - new_size,
                'confidence': self._calculate_confidence(current_candidates, candidate_tokens)
            })
            
            # Check convergence
            if new_size <= 1 or convergence_history[-1]['confidence'] >= confidence_threshold:
                break
        
        return {
            'final_candidates': current_candidates,
            'convergence_history': convergence_history,
            'seeds_used': used_seeds
        }
    
    def bayesian_triangulation(self, observations: Dict[int, Any],
                             candidate_tokens: List[str],
                             prior_probabilities: Dict[str, float] = None) -> Dict[str, float]:
        """
        Bayesian triangulation: combine observations with prior knowledge
        """
        if prior_probabilities is None:
            # Uniform prior if none provided
            prior = 1.0 / len(candidate_tokens)
            prior_probabilities = {token: prior for token in candidate_tokens}
        
        posterior_probs = prior_probabilities.copy()
        
        for seed, obs in observations.items():
            for token in candidate_tokens:
                # Compute likelihood P(observation | token)
                likelihood = self._compute_observation_likelihood(token, obs, seed)
                
                # Bayesian update
                posterior_probs[token] *= likelihood
            
        # Normalize probabilities
        total = sum(posterior_probs.values())
        if total > 0:
            posterior_probs = {k: v/total for k, v in posterior_probs.items()}
        
        return posterior_probs
    
    def robust_triangulation(self, observations: Dict[int, Any],
                           candidate_tokens: List[str],
                           outlier_threshold: float = 0.1) -> Dict[str, Any]:
        """
        Robust triangulation: detect and reject outlier observations
        """
        # Initial triangulation
        initial_solution = self.basic_triangulation(observations, candidate_tokens)
        
        # Identify outlier seeds
        outlier_seeds = self._detect_outlier_seeds(observations, initial_solution, candidate_tokens)
        
        if outlier_seeds:
            print(f"Detected {len(outlier_seeds)} outlier seeds: {outlier_seeds}")
            
            # Remove outliers and re-triangulate
            clean_observations = {seed: obs for seed, obs in observations.items() 
                                if seed not in outlier_seeds}
            robust_solution = self.basic_triangulation(clean_observations, candidate_tokens)
            
            return {
                'tokens': robust_solution,
                'outlier_seeds': outlier_seeds,
                'method': 'robust'
            }
        else:
            return {
                'tokens': initial_solution,
                'outlier_seeds': [],
                'method': 'basic'
            }
    
    def _get_consistent_tokens(self, observation: Any, 
                             candidate_tokens: List[str], 
                             seed: int) -> List[str]:
        """
        Check which candidate tokens are consistent with an observation
        In real implementation, this would check actual bit positions
        """
        # For demo purposes, we'll simulate this
        # Real implementation would use the actual HLL bit positions
        consistent_tokens = []
        
        for token in candidate_tokens:
            # Simulate consistency check - in reality, we'd compute the bit position
            # and check if it's set in the observation
            if self._simulate_consistency_check(token, observation, seed):
                consistent_tokens.append(token)
        
        return consistent_tokens
    
    def _simulate_consistency_check(self, token: str, observation: Any, seed: int) -> bool:
        """Simulate consistency check for demo purposes"""
        # In real implementation, this would:
        # 1. Compute bit position for token with given seed
        # 2. Check if that bit is set in the observation HLLSet
        # For now, we'll use a probabilistic simulation
        hash_val = hash(token + str(seed))
        return (hash_val % 100) < 85  # 85% chance of consistency
    
    def _compute_observation_likelihood(self, token: str, observation: Any, seed: int) -> float:
        """Compute likelihood of observation given token"""
        if self._simulate_consistency_check(token, observation, seed):
            return 0.95  # High likelihood if consistent
        else:
            return 0.05  # Low likelihood if inconsistent
    
    def _calculate_confidence(self, candidates: Set[str], all_tokens: List[str]) -> float:
        """Calculate confidence in triangulation result"""
        if not all_tokens:
            return 0.0
        return 1.0 - (len(candidates) / len(all_tokens))
    
    def _detect_outlier_seeds(self, observations: Dict[int, Any],
                            solution: Set[str],
                            candidate_tokens: List[str]) -> List[int]:
        """Detect seeds that don't agree with the consensus"""
        outlier_seeds = []
        
        for seed, obs in observations.items():
            # Check how many solution tokens are consistent with this seed
            consistent_count = 0
            for token in solution:
                if self._simulate_consistency_check(token, obs, seed):
                    consistent_count += 1
            
            consistency_ratio = consistent_count / len(solution) if solution else 0
            
            if consistency_ratio < 0.5:  # Threshold for outlier
                outlier_seeds.append(seed)
        
        return outlier_seeds