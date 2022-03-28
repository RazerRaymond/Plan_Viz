(define (domain logistics-strips)
  (:requirements :strips) 
  (:predicates 	
    (is-package ?o)
	(is-truck ?t)
    (is-location ?l)
	(is-airplane ?a)
    (is-hub ?hub)
	(in ?o1 ?o2))

(:action load-truck
  :parameters
   (?o
    ?t
    ?l)
  :precondition
   (and (is-package ?o) (is-truck ?t) (is-location ?l)
   (in ?t ?l) (in ?o ?l))
  :effect
   (and (not (in ?o ?l)) (in ?o ?t)))

(:action load-airplane
  :parameters
   (?o
    ?a
    ?l)
  :precondition
   (and (is-package ?o) (is-airplane ?a) (is-location ?l)
   (in ?o ?l) (in ?a ?l))
  :effect
   (and (not (in ?o ?l)) (in ?o ?a)))

(:action unload-truck
  :parameters
   (?o
    ?t
    ?l)
  :precondition
   (and (is-package ?o) (is-truck ?t) (is-location ?l)
        (in ?t ?l) (in ?o ?t))
  :effect
   (and (not (in ?o ?t)) (in ?o ?l)))

(:action unload-airplane
  :parameters
   (?o
    ?a
    ?l)
  :precondition
   (and (is-package ?o) (is-airplane ?a) (is-location ?l)
        (in ?o ?a) (in ?a ?l))
  :effect
   (and (not (in ?o ?a)) (in ?o ?l)))

(:action move-truck
  :parameters
   (?t
    ?l-from
    ?l-to
    ?l)
  :precondition
   (and (is-truck ?t) (is-location ?l-from) (is-location ?l-to) (is-location ?l)
   (in ?t ?l-from)
   (in ?l-from ?l)
   (in ?l-to ?l))
  :effect
   (and (not (in ?t ?l-from)) (in ?t ?l-to)))

(:action move-airplane
  :parameters
   (?a
    ?l-from
    ?l-to)
  :precondition
   (and (is-airplane ?a) (is-location ?l-from) (is-location ?l-to)
	(in ?a ?l-from))
  :effect
   (and (not (in ?a ?l-from)) (in ?a ?l-to)))
)
