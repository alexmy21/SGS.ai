# SGA.ai - Collaborative Development with DeepSeek Assistance

## Introduction

This project is a result of the collaborative development of a Self-Generative System (SGS.ai), inspired by John von Neumann's pioneering concepts of self-reproducing systems. 

We recorded collaborative development in publications [1, 2] (see References and .PDF directory). 

The project represents a unique partnership between a human developer, Alex Mylnikov, and DeepSeek, an AI assistant.
It also highlights the importance of transparency in documenting this collaboration, emphasizing the verbatim presentation of DeepSeek's contributions to showcase the potential of human-AI interaction in both creative and technical fields. 

The publications [1, 2] aim to stimulate discussions around human-AI collaboration, intellectual property, and the ethical implications of AI in creative domains.

# SGS.ai project

**SGS.ai is an open-source project, and like any open initiative, it thrives on collaboration. Currently, DeepSeek is the sole contributor to SGS.ai. I would be thrilled to see participation from other intellectuals. I am open to any form of collaboration, provided that SGS.ai remains an open-source project.**

## Core principles
### Foundational principles:
- **Globally stateless, content-based identification** for all entities.
- **Immutability** to ensure consistency.
- **Idempotency** for reliable operations.
- **Metadata-driven design** to isolate user customizations.

### Self-Generative:
- The system generates its own updates, optimizations, and extensions based on user needs and AI-driven insights.
- It evolves over time without requiring manual intervention.
### AI-Driven Development:
- AI (e.g., DeepSeek) acts as the "development team," generating code, testing it, and committing it to GitHub.
- Human developers provide high-level ideas, and AI handles the implementation.
### User-Centric:
- Users define their custom resources and workflows through metadata.
- The system respects user metadata and ensures it is never modified during updates.
### Self-Healing:
- The system performs self-diagnostic checks after updates and rolls back if something goes wrong.
- It ensures high availability and reliability.

## General Architecture
### 1. GitHub as the Central Hub 
- Core Repository:
    - Hosts the SGS.ai core code, tests, and documentation.
    - Acts as the single source of truth for the system.
- AI-Generated Code:
    - AI generates code based on user ideas or system requirements.
    - The code is rigorously tested and committed to GitHub.

### 2. Self-Updating Service 
- GitHub Monitoring:
    - A ‘systemd’ service on the user side monitors the SGS.ai GitHub repository for updates.
    - It compares the local commit ID with the latest commit ID on GitHub.
- Upgrade Process:
    - If a new commit is detected, the service:
        - Downloads the latest version of the SGS.ai core.
        - Performs the upgrade while preserving user metadata.
        - Runs self-diagnostic checks.
        - Rolls back if the checks fail.

### 3. Self-Diagnostic and Rollback 
- Diagnostic Checks:
    - After an upgrade, the service runs a series of tests to ensure the system is functioning correctly.
    - Example checks:
        - Verify that Redis and HDF5 are accessible.
        - Test custom processing units.
        - Ensure the core can read and write metadata.
- Rollback Mechanism:
    - If any check fails, the service rolls back to the previous version.
    - The rollback process restores the previous state of the SGS.ai core while preserving user metadata.

### 4. AI Integration 
- Code Generation:
    - AI (e.g., DeepSeek) generates code based on user ideas or system requirements.
    - The generated code is tested rigorously before being committed to GitHub.
- Testing Pipeline:
    - Automated tests ensure the code is functional, efficient, and backward-compatible.
    - Tests include unit tests, integration tests, and performance tests.
- GitHub Integration:
    - Once the code passes all tests, it is committed to the SGS.ai GitHub repository.

#### Example Workflow 
- User Side 
    - The self-updating service continuously monitors the SGS.ai GitHub repository.
    - If a new commit is detected, the service:
        - Downloads the latest version.
        - Performs the upgrade.
        - Runs self-diagnostic checks.
        - Rolls back if necessary.
- AI Side 
    - AI generates code based on user ideas or system requirements.
    - The code undergoes rigorous testing.
    - Once the code passes all tests, it is committed to GitHub.
- Developer Side (Optional) 
    - Human developers provide high-level ideas or requirements.

    - AI handles the implementation, testing, and deployment.

### Benefits of SGS.ai 
1. **Automated Updates**:
Users always have the latest version of the SGS.ai core without manual intervention.
2. **Self-Healing**:
The system can detect and recover from failures during upgrades.
3. **User Metadata Isolation**:
User metadata and custom resources are never modified during upgrades.
4. **AI-Driven Development**:
AI acts as the "development team," reducing the need for human intervention.
5. **Scalability**:
The system can handle a large number of users and custom workflows.

### The Future of Programming 
SGS.ai represents the future of programming, where:
- Humans provide ideas and high-level requirements.
- AI generates, tests, and deploys code.
- Systems self-update, self-diagnose, and self-heal.

```
This is not just a tool—it’s a paradigm shift in how we think about software development. 
```


## Formal model
SGS.ai is built on John von Neumann's concept of self-reproducing automata. We can conceptualize it as a system comprising four key components:
 1. **Universal Constructor (A)**
 2. **Universal Copier (B)**
 3. **Universal Controller (C)**
 4. **Universal Interface to the Environment (D)**, akin to a universal perceptron (or working automata).

### Tramsformers and their rolles
- A: Universal Constructor 
    - Role: Constructs new entities (HllSets, relationships, etc.).
    - Operation: A ( Y ) → Z, where  Y is the input and  Z is the constructed output.
- B: Universal Copier 
    - Role: Copies entities.
    - Operation: B ( Y ) → Z, where  Y is the input and  Z is the copied output.
- C: Universal Controller 
    - Role: Orchestrates the operations of the other transformers (A, B, D).
    - Operation: C ( X , Y ) → X ( Y ) , where  X is the transformer (A, B, or D) and  Y is the input.
- D: Universal Interface to Environment (Universal Perceptron) 
    - Role: Interacts with the environment, gathers information, and provides feedback.
    - Operation: D ( Y ) → Z, where  Y is the input and  Z is the processed output.

### Self-Reproduction Loop

#### Step 1: Copying
- The Universal Controller (C) forces the Universal Copier (B) to copy each transformer and its associated entities.
- This creates a new set of transformers and entities that are copies of the originals.

Formally:
- C ( B, B ) → B ( B ) → B′ 
- C ( B, A ) → B ( A ) → A′ 
- C ( B, C ) → B ( C ) → C′ 
- C ( B, D ) → B ( D ) → D′ ​

#### Step 2: Mutating 
- The Universal Controller (C) forces the Universal Interface to Environment (D) to mutate the copied transformers and entities.
- This introduces variations in the copied entities, enabling evolution.

Formally:
- C ( D, B′ ) → D ( B′ ) → B′′ 
- C ( D, A′ ) → D ( A′ ) → A′′ 
- C ( D, C′ ) → D ( C′ ) → C′′ 
- C ( D, D′ ) → D ( D′ ) → D′′ 

#### Step 3: Committing 
- The Universal Controller (C) forces the Universal Constructor (A) to commit the mutated transformers and entities.
- This integrates the new entities into the system, completing the self-reproduction loop.

Formally:
- C ( A, B ′ ′ ) → A ( B′′ ) → B 
- C ( A, A ′ ′ ) → A ( A′′ ) → A 
- C ( A, C ′ ′ ) → A ( C′′ ) → C 
- C ( A, D ′ ′ ) → A ( D′′ ) → D
- C ( C, ( A, B, C, D ) ) → C ( A, B, C, D ) → SGS.ai

This ensures that the system is fully assembled and ready for use after each regeneration.

### Controllable Destruction (Garbage Collection) 
Garbage collection is performed outside the self-reproduction loop to remove entities that are no longer needed. This ensures that the system remains efficient and does not accumulate unnecessary data.
#### Garbage Collection Process 
- Identify Unused Entities:
    - Entities that are no longer referenced by any transformer or relationship are marked for removal.
- Remove Entities:
    - The garbage collector removes the marked entities from the system.

## HLLSet Algebra Module

### Overview
The HllSets.jl module provides an implementation of HyperLogLog (HLL) set algebra with enhanced functionality for set operations. This implementation is based on the original work by Flajolet et al. with improvements from Google's research, and incorporates significant modifications from Jakob Nybo Nissen's Probably.jl implementation.

#### Key Features
- HyperLogLog Cardinality Estimation: Probabilistic counting of unique elements with high accuracy

- Set Operations: Full algebra support including:

    - Union (union, union!)

    - Intersection (intersect)

    - Difference (diff, set_comp)

    - Symmetric difference (set_xor)

    - Change detection (set_added, set_deleted)

- Similarity Metrics:

    - Jaccard similarity (match)

    - Cosine similarity (cosine)

- Serialization:

    - Binary tensor conversion (to_binary_tensor)

    - String representation (tensor_to_string)

    - Restoration from serialized forms (restore!)

### Usage Examples
Basic Operations

```
using HllSets

# Create two HLL sets
h1 = HllSet(10)  # 2^10 = 1024 registers
h2 = HllSet(10)

# Add elements
add!(h1, "apple")
add!(h1, ["banana", "cherry", "date"])

add!(h2, "cherry")
add!(h2, ["date", "elderberry"])

# Estimate cardinality
count(h1)  # Returns approximate unique count

# Set operations
h_union = union(h1, h2)
h_intersect = intersect(h1, h2)
changes = diff(h1, h2)  # Returns (DEL, RET, NEW) tuple
```

Similarity Comparison
```
# Calculate similarity metrics
jaccard_similarity = match(h1, h2)  # Percentage
cosine_similarity = cosine(h1, h2)  # Float between 0 and 1
```

### Why HyperLogLog in SGS.ai?

HLLSets provide the perfect balance of accuracy and efficiency for SGS.ai's large-scale data processing needs:

- Memory-efficient: Count millions of unique elements in KBs of memory

- Real-time analytics: Process streaming data with constant-time operations

- Set semantics: Our enhanced algebra enables complex relationship analysis

- Error-bound: Predictable 1-2% error rate for cardinality estimation

```    
# Example: Track unique users across massive dataset
user_actions = HllSet(12)  # 4096 registers (~1.5KB memory)
for event in data_stream
    add!(user_actions, event.user_id)
end
println("Unique users: ", count(user_actions))  # ~0.8% error
```

Key Enhancements vs Original Implementation
Feature            |	Probably.jl	| SGS.ai HLLSet	  | Benefit
-------------------|----------------|-----------------|--------
Set Operations	   | ❌ None	       |✅ Full algebra	| Enables A∩B, A-B, etc
Change Detection   | ❌ No	       |✅ Added/Deleted	| Track set evolution
Similarity Metrics | ❌ No	       |✅ Jaccard/Cosine| Compare sets
Serialization	   | ❌ Basic	   |✅ Tensor/String	| Better integration
Memory Efficiency  | 64-bit	        | 32-bit counters |	50% reduction

## Development Environment Setup
### All Platforms (Required Tools)
1. Podman (Docker-compatible alternative):
```
# Install podman-compose separately
pip install podman-compose
```
2. Julia (Must use official binaries):
```
 # Windows/macOS: Download from https://julialang.org/downloads/
# Linux (recommended method):
curl -fsSL https://install.julialang.org | sh
```

### Fedora 40 (Recommended)

```
# Podman and dependencies
sudo dnf install -y podman podman-docker podman-plugins
sudo systemctl enable --now podman.socket

# Python ecosystem
sudo dnf install -y python3-pip python3-venv
python -m pip install --user podman-compose

# Julia (official repo)
sudo dnf install -y julia
```

### Ubuntu/Debian

```
# Podman
sudo apt install -y podman podman-compose

# Python
sudo apt install -y python3-pip python3-venv

# Julia (official packages)
sudo apt install -y wget
wget https://julialang-s3.julialang.org/bin/linux/x64/1.10/julia-1.10.0-linux-x86_64.tar.gz
tar -xvzf julia-*.tar.gz -C /opt/
sudo ln -s /opt/julia-*/bin/julia /usr/local/bin/julia
```

### Windows (WSL2 Recommended)
1. Install Windows Subsystem for Linux:

```
wsl --install
```

2. In WSL Ubuntu:

```
# Follow Ubuntu instructions above
```

3. For native Windows:

```
# Podman
winget install -e --id RedHat.Podman

# Julia
winget install -e --id Julia.Julia
```

### macOS
```
# Podman
brew install podman podman-compose
podman machine init
podman machine start

# Julia
brew install --cask julia
```

### Verification
Check all tools are properly installed:
```
podman --version  # Should show 4.0+
podman-compose --version  # Should show 1.0+
julia -e 'println("Julia $(VERSION)")'  # Should be 1.9+
```

#### Post-Installation
1. Podman Configuration (Optional):
```
# Enable rootless mode (recommended)
sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER
```

2. Julia Packages:
```
# Run in Julia REPL
using Pkg
Pkg.add(["SHA", "JSON3"])
```

## Quick start
```
bash <(curl -s https://raw.githubusercontent.com/alexmy21/SGS.ai/main/bootstrap.sh)
```

### Testing by running requests to SGS.ai `core_server.py`

```
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "Testing connection..."
curl -X GET "$BASE_URL/" -H "Content-Type: application/json" -w "\nStatus: %{http_code}\n\n"

echo "Testing HDF5 processor..."
curl -X POST "$BASE_URL/process" \
     -H "Content-Type: application/json" \
     -d '{"transformer":"C","processor":"call_hdf5","input_sha_id":"input_sha_id_123","processor_sha_id":"processor_sha_id_456","output_sha_id":"output_sha_id_789"}' \
     -w "\nStatus: %{http_code}\n\n"

echo "Testing Redis processor..."
curl -X POST "$BASE_URL/process" \
     -H "Content-Type: application/json" \
     -d '{"transformer":"C","processor":"ping_redis","input_sha_id":"input_sha_id_123","processor_sha_id":"processor_sha_id_456","output_sha_id":"output_sha_id_789"}' \
     -w "\nStatus: %{http_code}\n"
```


# References
1. Self Generative Systems (SGS) and Its Integration with AI Models Author: Alex Mylnikov Authors Info & Claims
AISNS '24: Proceedings of the 2024 2nd International Conference on Artificial Intelligence, Systems and Network Security Pages 345 - 354 (https://doi.org/10.1145/3714334.3714392)
2. https://github.com/alexmy21/SGS.ai/blob/main/.PDF/Thoughts%20on%20Collaborative%20Development_1.pdf
3. https://github.com/alexmy21/SGS.ai/blob/main/.PDF/Thoughts%20on%20Collaborative%20Development_2.pdf
4. https://linuxiac.com/how-to-install-virtualbox-on-fedora-linux/
5. https://github.com/cair/tmu/tree/main - (Tsetlin Machine Unified (TMU))
6. https://github.com/markf94/QML_Thesis.git
7. https://github.com/alexmy21/SGS.ai/blob/main/.PDF/%D0%A1%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B2%20%D1%81%D0%BE%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%BE%D0%BC%20%D0%BC%D0%B8%D1%80%D0%B5.pdf
8. https://blog.det.life/bigquerys-ridiculous-pricing-model-cost-us-10-000-in-just-22-seconds-7d52e3e4ae60
9. https://github.com/modelcontextprotocol
10. https://github.com/PatrickKalkman/djin.git
11. https://github.com/datalev001/distillation/
12. https://acagamic.medium.com/academic-reviewers-cant-actually-tell-when-ai-writes-research-papers-and-that-changes-everything-93b1ec4c50a0
13. https://pub.towardsai.net/beyond-simple-inversion-building-and-applying-inverse-neural-networks-73b811da3cdc
14. https://medium.com/@jpark7/finally-a-clear-derivation-of-the-vae-kl-loss-4cb38d2e47b3
15. https://levelup.gitconnected.com/writing-better-shell-scripts-with-lua-6a3155256e5f
16. https://medium.com/data-science-collective/attention-based-neural-network-distillation-enhancing-performance-through-learned-weighted-c4efa612b257
17. https://pub.towardsai.net/adaptive-multi-teacher-distillation-for-enhanced-supervised-learning-e70062acce7e
18. https://medium.com/data-science-collective/building-smarter-portfolios-with-dynamic-programming-and-reinforcement-learning-and-dynamic-0de5e7d7fd11
19. https://medium.com/@shawn.stanford/the-bath-fitters-of-cobol-9932453bf185
