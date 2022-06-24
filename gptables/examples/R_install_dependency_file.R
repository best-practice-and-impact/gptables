#' install packages from a list
#' 
#' @description install any packages from a list of packages which R does not have
#' 
#' @param pkglist list of packages to install
#' 
#' @return NA 
#'  
#' @export 

packageRefresh <- function(pkglist) {
  if(length(names(sessionInfo()$otherPkgs))) {
    lapply(names(sessionInfo()$otherPkgs), function(pkgs) detach(paste0("package:", pkgs), 
                                                                 character.only = T))
  }
  newPackages <- pkglist[!(pkglist %in% installed.packages()[,"Package"])]
  if(length(newPackages)) {
    install.packages(newPackages)
  }
  }