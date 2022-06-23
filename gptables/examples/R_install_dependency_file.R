packagesReq <- c("dplyr", "reticulate", "magrittr")
packageRefresh <- function(pkgList) {
  if(length(names(sessionInfo()$otherPkgs))) {
    lapply(names(sessionInfo()$otherPkgs), function(pkgs) detach(paste0("package:", pkgs), 
                                                                 character.only = T))
  }
  newPackages <- pkgList[!(pkgList %in% installed.packages()[,"Package"])]
  if(length(newPackages)) {
    install.packages(newPackages)
  }
  }