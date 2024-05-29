# PBL6-PAM Scripts

## Scripts usage:
**Windows**:
```
bash ./scripts/ ...
```
You need turned on Docker Desktop.

**Linux**:
```
./scripts/ ...
```

#### build_and_push_all.sh
Builds and pushes images based on Dockerfiles from every subdirectory.
```
cd Projekt_PBL6 
bash ./scripts/build_and_push_all.sh
```

#### single_build_and_push.sh
Builds and pushes image based on Dockerfile from chosen subdirectory.
```
cd Projekt_PBL6 
bash ./scripts/single_build_and_push.sh ./pubsub
```

#### Potential problems
If while running you encounter:
```
./scripts/build_and_push_all.sh: line 2: $'\r': command not found
```
change "End of Line" sequence in VS Code to "LF".